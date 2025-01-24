from abc import abstractmethod
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel
from pathlib import Path
import json


class EmailMessage(BaseModel):
    subject: str
    sender: str
    to: Optional[str]
    cc: Optional[str]
    date: datetime
    body: str
    attachments: List[Dict[str, str | None]]
    message_id: str
    provider: str


class BaseEmailFetcher:
    def __init__(self, storage_path: str = "emails"):
        """
        Initialize the email fetcher with storage path configuration.

        Args:
            storage_path: Directory path where emails will be stored
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _save_email(self, email_data: EmailMessage) -> None:
        """
        Save email data to JSON file.

        Args:
            email_data: EmailMessage object containing email information
        """
        email_dict = {
            "subject": email_data.subject,
            "sender": email_data.sender,
            "to": email_data.to,
            "cc": email_data.cc,
            "date": email_data.date.isoformat(),
            "body": email_data.body,
            "attachments": email_data.attachments,
            "message_id": email_data.message_id,
            "provider": email_data.provider
        }

        filename = f"{email_data.date.strftime('%Y%m%d_%H%M%S')}_{email_data.message_id}.json"
        filepath = self.storage_path / email_data.provider / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(email_dict, f, ensure_ascii=False, indent=2)

    @abstractmethod
    def fetch_emails(self, days: int = 3) -> List[EmailMessage]:
        pass
