from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel
from common.logger import get_logger
from data_loader.base_email_fetcher import EmailMessage
from llm.clients.base_llm_client import BaseLLMClient
from llm.templates.message_digest.information_extraction import InformationExtractionPrompt
from llm.templates.message_digest.email_summarizing import EmailSummarizingPrompt


logger = get_logger(__name__)


class SourceMessage(BaseModel):
    date: datetime
    summary: str


class Memo(BaseModel):
    type: Literal["actionable", "informative"]
    source: SourceMessage
    details: str
    summary: str


class MemoboardBuilder:
    def __init__(self, llm_client: BaseLLMClient, persona: str):
        self.llm_client = llm_client
        self.persona = persona

    def read_email(self, email: EmailMessage) -> List[Memo]:
        summary_result = self.llm_client.prompt(
            template=EmailSummarizingPrompt,
            template_params={
                "persona": self.persona,
                "subject": email.subject,
                "date": email.date,
                "sender": email.sender,
                "recipient": email.to,
                "content": email.body,
            },
        )
        extraction_result = self.llm_client.prompt(
            template=InformationExtractionPrompt,
            template_params={
                "persona": self.persona,
                "subject": email.subject,
                "date": email.date,
                "sender": email.sender,
                "recipient": email.to,
                "summary": summary_result.summary,
            }
        )
        return [
            Memo(
                type=extraction.type,
                source=SourceMessage(date=email.date, summary=summary_result.summary),
                details=extraction.details,
                summary=summary_result.summary,
            )
            for extraction in extraction_result.extractions
        ]
