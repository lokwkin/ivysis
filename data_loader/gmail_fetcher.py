import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from typing import List
from dateutil import parser
import base64
from common.logger import get_logger

from data_loader.base_email_fetcher import BaseEmailFetcher, EmailMessage

logger = get_logger(__name__)


class GmailFetcher(BaseEmailFetcher):
    def __init__(self, email: str, password: str, storage_path: str = "emails"):
        """
        Initialize Gmail fetcher with credentials.

        Args:
            email: Gmail email address
            password: App-specific password or account password
            storage_path: Directory path where emails will be stored
        """
        super().__init__(storage_path)
        self.email = email
        self.password = password
        self.imap_server = "imap.gmail.com"

    def fetch_emails(self, days: int = 3) -> List[EmailMessage]:
        try:
            # Connect to Gmail
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email, self.password)
            mail.select('INBOX')

            # Calculate date range
            date_from = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")

            # Search for emails within date range
            _, messages = mail.search(None, f'(SINCE {date_from})')
            email_messages = []

            for num in messages[0].split():
                _, msg_data = mail.fetch(num, '(RFC822)')
                email_body = msg_data[0][1]
                email_msg = email.message_from_bytes(email_body)

                # Process email
                subject = decode_header(email_msg["Subject"])[0][0]
                subject = subject if isinstance(subject, str) else subject.decode()
                sender = email_msg["From"]
                date = parser.parse(email_msg["Date"])

                # Get body and attachments
                body = ""
                attachments = []

                for part in email_msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                    elif part.get_content_maintype() != 'multipart':
                        attachment_data = {
                            "filename": part.get_filename(),
                            "content_type": part.get_content_type(),
                            "data": base64.b64encode(part.get_payload(decode=True)).decode()
                        }
                        attachments.append(attachment_data)

                email_message = EmailMessage(
                    subject=subject,
                    sender=sender,
                    date=date,
                    body=body,
                    attachments=attachments,
                    message_id=email_msg["Message-ID"],
                    provider="gmail"
                )

                self._save_email(email_message)
                email_messages.append(email_message)

            mail.logout()
            return email_messages

        except Exception as e:
            logger.error(f"Error fetching Gmail: {str(e)}")
            raise
