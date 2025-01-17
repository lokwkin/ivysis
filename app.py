
from llm.ollama_client import OllamaClient
from llm.templates.email_classifier import EMAIL_CLASSIFIER


llm_client = OllamaClient(default_model="qwen2.5:7b")

llm_result = llm_client.prompt(
    template=EMAIL_CLASSIFIER,
    template_params={
        "subject": "Re: Budget Control Meeting 14 Jan Reminder",
        "sender": "finance@company.com"
    },
)
