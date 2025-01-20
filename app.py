
import datetime
import json
from data_loader.gmail_fetcher import GmailFetcher
from llm.ollama_client import OllamaClient
from llm.templates.biography_formation import BIOGRAPHY_FORMATION
import argparse
from llm.templates.email_uniqueness import EMAIL_UNIQUENESS

from llm.templates.persona_extraction import PERSONA_EXTRACTION

parser = argparse.ArgumentParser()
parser.add_argument("--email", required=True, help="Email address")
parser.add_argument("--password", required=True, help="Password")
args = parser.parse_args()


# Setup Gmail connection
gmail_fetcher = GmailFetcher(email=args.email, password=args.password)

# Setup LLM client
llm_client = OllamaClient(default_model="qwen2.5:7b")

# Fetch emails from Gmail
gmail_messages = gmail_fetcher.fetch_emails(days=3)


implications = []
for gmail_message in gmail_messages:
    print(gmail_message.subject, gmail_message.sender, gmail_message.date)
    persona_extraction_result = llm_client.prompt(
        template=PERSONA_EXTRACTION,
        template_params={
            "subject": gmail_message.subject,
            "date": gmail_message.date,
            "sender": gmail_message.sender,
            "body": gmail_message.body,
        },
    )

    email_uniqueness_result = llm_client.prompt(
        template=EMAIL_UNIQUENESS,
        template_params={
            "subject": gmail_message.subject,
            "date": gmail_message.date,
            "sender": gmail_message.sender,
        },
    )
    implications.extend(
        {
            "description": implication.description,
            "weight": email_uniqueness_result.score,
        }
        for implication in persona_extraction_result.implications
    )

with open(f"implications_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json", "w") as f:
    json.dump(implications, f, indent=2)


llm_result = llm_client.prompt(
    template=BIOGRAPHY_FORMATION,
    template_params={"implications": implications},
)
print(llm_result.description)
