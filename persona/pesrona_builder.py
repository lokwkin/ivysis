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

    persona_hypothesis_list: List[PersonaHypothesis]

    def __init__(self, llm_client: BaseLLMClient, storage_path: str):
        self.llm_client = llm_client
        self.email_batch_size = 10
        self.persona_hypothesis_list = []
        self.storage_path = storage_path

        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def digest_emails(self, emails: List[EmailMessage]):

        # split emails into batches
        email_batches = [emails[i:i + self.email_batch_size] for i in range(0, len(emails), self.email_batch_size)]

        for email_batch in email_batches:

            params = {
                "emails": [{
                    "idx": idx,
                    "subject": email.subject,
                    "date": email.date,
                    "sender": email.sender,
                    "recipient": email.to,
                } for idx, email in enumerate(email_batch)]}

            persona_extraction_batch_result = self.llm_client.prompt(
                template=PersonaExtractionBatchPrompt,
                template_params=params
            )

            email_uniqueness_result = self.llm_client.prompt(
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
                    self.implications.append(PersonaHypothesis(
                        category=implication.category,
                        description=implication.description,
                        weight=mapped_uniqueness_email.score,
                    ))

        with open(f"{self.storage_path}/implications.json", "w") as f:
            json.dump(self.implications, f, indent=2)

    def load_implications(self, implication_path: str):
        with open(implication_path, "r") as f:
            self.persona_hypothesis_list = [PersonaHypothesis(**item) for item in json.load(f)]

    def write_biography(self):

        markdown = ""

        # Group implications by category
        hypoethesis_by_category: Dict[str, List[PersonaHypothesis]] = {}
        for hypothesis in self.persona_hypothesis_list:
            if hypothesis.category not in hypoethesis_by_category:
                hypoethesis_by_category[hypothesis.category] = []
            hypoethesis_by_category[hypothesis.category].append(hypothesis)

        for category, hypothesis_list in hypoethesis_by_category.items():
            # Sort implications by weight in descending order
            sorted_hypothesis = sorted(hypothesis_list, key=lambda x: x.weight, reverse=True)

            # Keep top 50% of implications
            num_to_keep = max(1, len(sorted_hypothesis) // 2)  # Keep at least 1
            hypothesis_list = sorted_hypothesis[:num_to_keep]
            llm_result = self.llm_client.prompt(
                template=BiographyFormationPrompt,
                template_params={"implications": hypothesis_list},
            )
            markdown += f"## {category}\n\n{llm_result.description}\n\n"

        biography_writing_result = self.llm_client.prompt(
            template=BiographyWritingPrompt,
            template_params={"draft": markdown},
        )

        with open(f"{self.storage_path}/biography.txt", "w") as f:
            f.write(biography_writing_result.biography)
