from datetime import datetime
from typing import List, Literal
from uuid import uuid4
from pydantic import BaseModel
from common.logger import get_logger
from common.utils import safe_write_file
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
    categories: List[str]
    details: str
    summary: str


class MemoboardBuilder:
    def __init__(self, llm_client: BaseLLMClient, persona: str, storage_path: str):
        self.llm_client = llm_client
        self.persona = persona
        self._storage_path = f"{storage_path}/memoboard"

    def process_email(self, email: EmailMessage) -> List[Memo]:
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

        memos: List[Memo] = []
        for extraction in extraction_result.extractions:
            memo = Memo(
                type=extraction.type,
                source=SourceMessage(date=email.date, summary=summary_result.summary),
                categories=extraction.categories,
                details=extraction.details,
                summary=summary_result.summary,
            )
            self._save_memo(memo)
            memos.append(memo)
        return memos

    def _save_memo(self, memo: Memo):
        for category in memo.categories:
            uuid = str(uuid4())
            file_path = f"{self._storage_path}/{category}/{str(uuid)[:8]}.json"
            safe_write_file(file_path, memo.model_dump_json())
