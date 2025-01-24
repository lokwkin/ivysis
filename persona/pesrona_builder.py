import json
import os
from typing import Dict, List
from common.logger import get_logger

from data_loader.base_email_fetcher import EmailMessage
from llm.ollama_client import OllamaClient
from llm.templates.onboarding.biography_formation import BiographyFormationPrompt
from llm.templates.onboarding.email_uniqueness_batch import EmailUniquenessPrompt
from llm.templates.onboarding.persona_extraction_batch import PersonaExtractionBatchPrompt


logger = get_logger(__name__)


class PersonaBuilder:

    implications: List[Dict[str, str]]

    def __init__(self, storage_path: str):
        self.llm_client = OllamaClient(default_model="qwen2.5:7b")
        self.email_batch_size = 10
        self.implications = []
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
                    self.implications.append(
                        {
                            "subject": input_email.subject,
                            "category": implication.category,
                            "description": implication.description,
                            "weight": mapped_uniqueness_email.score,
                        }
                    )

        with open(f"{self.storage_path}/implications.json", "w") as f:
            json.dump(self.implications, f, indent=2)

    def load_implications(self, implication_path: str):
        with open(implication_path, "r") as f:
            self.implications = json.load(f)

    def write_biography(self):
        top_implications = list(filter(lambda x: x["weight"] >= 4, self.implications))

        llm_result = self.llm_client.prompt(
            template=BiographyFormationPrompt,
            template_params={"implications": top_implications},
        )

        with open(f"{self.storage_path}/biography.txt", "w") as f:
            f.write(llm_result.description)
        return llm_result.description
