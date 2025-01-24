
import datetime
from data_loader.gmail_fetcher import GmailFetcher
from llm.ollama_client import OllamaClient
import argparse
from persona.pesrona_builder import PersonaBuilder

parser = argparse.ArgumentParser()
parser.add_argument("--email", required=False, help="Email address")
parser.add_argument("--password", required=False, help="Password")
parser.add_argument("--days", required=False, default=3, help="Days")
parser.add_argument("--load_implications", required=False, default=None, help="Load implications from file")

args = parser.parse_args()

# Setup LLM client
llm_client = OllamaClient(default_model="internlm3-8b-instruct")

storage_folder = f"./data/{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}"

persona_builder = PersonaBuilder(storage_path=storage_folder)

if args.email and args.password:

    # Fetch emails from Gmail
    gmail_fetcher = GmailFetcher(email=args.email, password=args.password, storage_path=storage_folder)
    gmail_messages = gmail_fetcher.fetch_emails(days=args.days)
    persona_builder.digest_emails(gmail_messages)

    biography = persona_builder.write_biography()
    print(biography)

elif args.load_implications:
    # Load implications from file
    persona_builder.load_implications(args.load_implications)

    biography = persona_builder.write_biography()
    print(biography)

else:
    parser.print_help()
    exit(1)
