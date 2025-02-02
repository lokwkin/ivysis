import json
import os
from typing import Dict, List

from pydantic import BaseModel
from common.logger import get_logger

from data_loader.base_email_fetcher import EmailMessage
from llm.clients.base_llm_client import BaseLLMClient
from llm.templates.onboarding.biography_formation import BiographyFormationPrompt
from llm.templates.onboarding.biography_writing import BiographyWritingPrompt
from llm.templates.onboarding.email_uniqueness_batch import EmailUniquenessPrompt
from llm.templates.onboarding.persona_extraction_batch import PersonaExtractionBatchPrompt


logger = get_logger(__name__)


class PersonaHypothesis(BaseModel):
    category: str
    description: str
    weight: int

    class Config:
        extra = 'allow'


class PersonaBuilder:
    """
    Build text persona description from messages history.
    """

    persona_hypothesis_list: List[PersonaHypothesis]

    def __init__(self, llm_client: BaseLLMClient, storage_path: str):
        self._llm_client = llm_client
        self._email_batch_size = 10
        self._persona_hypothesis_list = []
        self._storage_path = storage_path
        self._persona = None

    def get_persona(self):
        return self._persona

    def digest_emails(self, emails: List[EmailMessage]):
        """
        Digest emails into persona hypothesis by batches.
        All the hypothesis will be stored accumulatively.
        After each batch run, it will generate a biography with all accumulated hypothesis, and create a persona checkpoint.

        Note: should call _load_hypothesis() to load previous data into the instance first.
        """
        email_batches = [emails[i:i + self._email_batch_size] for i in range(0, len(emails), self._email_batch_size)]

        for idx, email_batch in enumerate(email_batches):
            # Process emails and batch hypothesis
            batch_hypothesis = self._process_emails(email_batch)
            self._persona_hypothesis_list.extend(batch_hypothesis)
            self._save_hypothesis(idx)

            # Write biography with all accumulated hypothesis
            self._persona = self._write_persona(self._persona_hypothesis_list)
            self._save_persona(idx)

    def _process_emails(self, email_batch: List[EmailMessage]) -> List[PersonaHypothesis]:
        """
        Process email headers including subject, sender and recipient to extract implication from the email. 
        Return a list of hypothesis to the user persona.
        """

        hypothesis_list: List[PersonaHypothesis] = []
        params = {
            "emails": [{
                "idx": idx,
                "subject": email.subject,
                "date": email.date,
                "sender": email.sender,
                "recipient": email.to,
            } for idx, email in enumerate(email_batch)]}

        persona_extraction_batch_result = self._llm_client.prompt(
            template=PersonaExtractionBatchPrompt,
            template_params=params
        )

        email_uniqueness_result = self._llm_client.prompt(
            template=EmailUniquenessPrompt,
            template_params=params
        )

        for idx, input_email in enumerate(email_batch):

            # Map the referenced email with the input email using "idx" field
            mapped_implication_email = next((e for e in persona_extraction_batch_result.emails if e.idx == idx), None)
            mapped_uniqueness_email = next((e for e in email_uniqueness_result.emails if e.idx == idx), None)

            if mapped_uniqueness_email is None or mapped_implication_email is None:
                logger.error(f"Email {idx} not found in the result")
                continue

            for implication in mapped_implication_email.implications:
                hypothesis_list.append(PersonaHypothesis(
                    category=implication.category,
                    description=implication.description,
                    weight=mapped_uniqueness_email.score,
                ))

        return hypothesis_list

    def _write_persona(self, hypothesis_list: List[PersonaHypothesis]) -> str:
        """
        Write a biography with all accumulated hypothesis.
        """

        markdown = ""

        # Group implications by category
        hypoethesis_by_category: Dict[str, List[PersonaHypothesis]] = {}
        for hypothesis in hypothesis_list:
            if hypothesis.category not in hypoethesis_by_category:
                hypoethesis_by_category[hypothesis.category] = []
            hypoethesis_by_category[hypothesis.category].append(hypothesis)

        for category, hypothesis_list in hypoethesis_by_category.items():
            # Sort implications by weight in descending order
            sorted_hypothesis = sorted(hypothesis_list, key=lambda x: x.weight, reverse=True)

            # Keep top 50% of implications
            num_to_keep = max(1, len(sorted_hypothesis) // 2)  # Keep at least 1
            hypothesis_list = sorted_hypothesis[:num_to_keep]
            llm_result = self._llm_client.prompt(
                template=BiographyFormationPrompt,
                template_params={"implications": hypothesis_list},
            )
            markdown += f"## {category}\n\n{llm_result.description}\n\n"

        biography_writing_result = self._llm_client.prompt(
            template=BiographyWritingPrompt,
            template_params={"draft": markdown},
        )

        return biography_writing_result.biography

    def _save_persona(self, checkpoint_idx: int) -> None:
        """
        Save the biography into local storage.
        """
        checkpoint_dir = f"{self._storage_path}/checkpoint_{checkpoint_idx}"
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        with open(f"{checkpoint_dir}/persona.txt", "w") as f:
            f.write(self._persona)

    def _save_hypothesis(self,  checkpoint_idx: int) -> None:
        """
        Save hypothesis list into local storage with a specific checkpoint index.
        """
        checkpoint_dir = f"{self._storage_path}/checkpoint_{checkpoint_idx}"
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        with open(f"{checkpoint_dir}/hypothesis.json", "w") as f:
            json.dump([i.model_dump() for i in self._persona_hypothesis_list], f, indent=2)

    def load_checkpoint(self, checkpoint_path: str) -> None:
        """
        Load hypothesis list from the local storage with a specific checkpoint index.
        """
        with open(f"{checkpoint_path}/hypothesis.json", "r") as f:
            self._persona_hypothesis_list = [PersonaHypothesis(**item) for item in json.load(f)]
        with open(f"{checkpoint_path}/persona.txt", "r") as f:
            self._persona = f.read()
