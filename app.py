from memoboard.memoboard_builder import MemoboardBuilder
from persona.pesrona_builder import PersonaBuilder
from llm.clients.ollama_client import OllamaClient
import os
import argparse
from llm.clients.groq_client import GroqClient
from data_loader.gmail_fetcher import GmailFetcher
from data_loader.base_email_fetcher import EmailMessage
import datetime
from dotenv import load_dotenv
import sys

load_dotenv(override=True)

# from llm.ollama_client import OllamaClient


parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description="Personal AI Assistant")
subparsers = parser.add_subparsers(dest="command", help="Available commands")

# Persona builder command
persona_parser = subparsers.add_parser("persona", help="Build or update persona")
persona_parser.add_argument("--email_addr", required=False, help="Email address")
persona_parser.add_argument("--email_pwd", required=False, help="Email password")
persona_parser.add_argument("--load_checkpoint", required=False, help="Checkpoint directory path")
persona_parser.add_argument("--days", type=int, default=3, help="Number of days to fetch emails")

# Memoboard builder command
memoboard_parser = subparsers.add_parser("memoboard", help="Build memoboard")
memoboard_parser.add_argument("--load_persona", required=True, help="Path to persona data")
memoboard_parser.add_argument("--email", required=True, help="Path to email JSON file")

args = parser.parse_args()

if args.command is None:
    parser.print_help()
    sys.exit(1)

# Setup LLM client
if os.getenv("LLM_PROVIDER") == "ollama":
    llm_client = OllamaClient(default_model=os.getenv("OLLAMA_MODEL") or "qwen2.5:7b")
elif os.getenv("LLM_PROVIDER") == "groq":
    llm_client = GroqClient(api_key=os.getenv("GROQ_API_KEY"), default_model=os.getenv("GROQ_MODEL") or "llama-3.1-8b-instant")


data_dir = f"./data/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"


persona_desc = None

# Handle Build Persona command
if args.command == "persona":
    persona_builder = PersonaBuilder(llm_client=llm_client, storage_path=data_dir)

    if args.load_checkpoint:
        persona_builder.load_checkpoint(args.load_checkpoint)

    if args.email_addr and args.email_pwd:
        gmail_fetcher = GmailFetcher(
            email=args.email_addr,
            password=args.email_pwd,
            storage_path=data_dir
        )
        gmail_messages = gmail_fetcher.fetch_emails(days=args.days)
        persona_builder.digest_emails(gmail_messages)

    persona_desc = persona_builder.get_persona()


elif args.command == "memoboard":
    with open(args.load_persona, "r") as file:
        persona_desc = file.read()

    with open(args.email, "r") as file:
        email_content = EmailMessage.model_validate_json(file.read())

    memoboard_builder = MemoboardBuilder(llm_client, persona_desc, data_dir)
    memos = memoboard_builder.process_email(email_content)

else:
    print("Invalid command")
    parser.print_help()
    sys.exit(1)
