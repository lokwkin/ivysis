from typing import Optional
import ollama
from llm.clients.base_llm_client import BaseLLMClient
from llm.schemas.base import LLMRequest, LLMResponse, LLMTokenUsage
from common.logger import get_logger

logger = get_logger(__name__)


class OllamaClient(BaseLLMClient):
    def __init__(self, host: Optional[str] = None, default_model: Optional[str] = None):
        """Initialize Ollama client with optional host configuration.

        Args:
            host: Optional host URL for Ollama server (e.g., 'http://localhost:11434')
        """
        super().__init__()
        if host:
            ollama.set_host(host)
        if default_model:
            self.default_model = default_model
        else:
            self.default_model = "qwen2.5:7b"

    def _request(self, prompt_input: LLMRequest) -> LLMResponse:
        """Execute request to Ollama server.

        Args:
            prompt_input: LLMRequest containing the prompt configuration

        Returns:
            LLMRawResponse with the model's response and token usage
        """
        response = ollama.generate(
            model=prompt_input.model,
            prompt=prompt_input.user_message,
            system=prompt_input.system_message,
            format="json"
        )

        token_usage = LLMTokenUsage(
            input_token=response.get('prompt_eval_count', 0),
            output_token=response.get('eval_count', 0)
        )

        return LLMResponse(
            response_str=response['response'],
            token_usage=token_usage
        )
