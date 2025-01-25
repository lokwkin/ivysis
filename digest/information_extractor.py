from common.logger import get_logger
from data_loader.base_email_fetcher import EmailMessage
from llm.clients.base_llm_client import BaseLLMClient
from llm.templates.information_extraction.email_extraction import InformationExtractionPrompt


logger = get_logger(__name__)


class InformationExtractor:
    def __init__(self, llm_client: BaseLLMClient, persona: str):
        self.llm_client = llm_client
        self.persona = persona

    def digest(self, email: EmailMessage):
        extraction_result = self.llm_client.prompt(
            template=InformationExtractionPrompt,
            template_params={
                "persona": self.persona,
                "subject": email.subject,
                "date": email.date,
                "sender": email.sender,
                "recipient": email.to,
                "content": email.body,
            }
        )
        return extraction_result.extractions
