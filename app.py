
import datetime
from data_loader.base_email_fetcher import EmailMessage
from data_loader.gmail_fetcher import GmailFetcher
from digest.information_extractor import InformationExtractor
from llm.clients.groq_client import GroqClient
# from llm.ollama_client import OllamaClient
import argparse
import os
from llm.clients.ollama_client import OllamaClient
from persona.pesrona_builder import PersonaBuilder
from dotenv import load_dotenv

load_dotenv()


parser = argparse.ArgumentParser()
parser.add_argument("--email", required=False, help="Email address")
parser.add_argument("--password", required=False, help="Password")
parser.add_argument("--days", required=False, default=3, help="Days", type=int)
parser.add_argument("--load_implications", required=False, default=None, help="implications file path")
parser.add_argument("--load_biography", required=False, default=None, help="Biography file path", type=str)
parser.add_argument("--digest_email", required=False, default=False, help="Email json file path", type=str)
args = parser.parse_args()

# Setup LLM client
if os.getenv("LLM_PROVIDER") == "ollama":
    llm_client = OllamaClient(default_model=os.getenv("OLLAMA_MODEL") or "internlm3-8b-instruct")
elif os.getenv("LLM_PROVIDER") == "groq":
    llm_client = GroqClient(api_key=os.getenv("GROQ_API_KEY"), default_model=os.getenv("GROQ_MODEL") or "llama-3.1-8b-instant")

storage_folder = f"./data/{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}"

persona_builder = PersonaBuilder(llm_client=llm_client, storage_path=storage_folder)

biography = None

if args.email and args.password:

    # Fetch emails from Gmail
    gmail_fetcher = GmailFetcher(email=args.email, password=args.password, storage_path=storage_folder)
    gmail_messages = gmail_fetcher.fetch_emails(days=args.days)
    persona_builder.digest_emails(gmail_messages)
    biography = persona_builder.write_biography()

elif args.load_implications:
    # Load implications from file
    persona_builder.load_implications(args.load_implications)
    biography = persona_builder.write_biography()


if not biography and args.load_biography:
    with open(args.load_biography, "r") as file:
        biography = file.read()

if args.digest_email:
    with open(args.digest_email, "r") as file:
        email_content = EmailMessage.model_validate_json(file.read())

    information_extractor = InformationExtractor(llm_client, biography)
    extractions = information_extractor.digest(email_content)
    print(extractions)
