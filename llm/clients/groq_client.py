from typing import Optional
from groq import Groq
from llm.clients.base_llm_client import BaseLLMClient
from llm.schemas.base import LLMRequest, LLMResponse, LLMTokenUsage
from common.logger import get_logger

logger = get_logger(__name__)


class GroqClient(BaseLLMClient):

    client: Groq
    default_model: str

    def __init__(self, api_key: str, default_model: Optional[str] = None):
        """Initialize Groq client with optional API key configuration.

        Args:
            api_key: Groq API key. If not provided, will look for GROQ_API_KEY environment variable
            default_model: Optional default model to use. If not provided, uses mixtral-8x7b-32768
        """
        super().__init__()
        self.client = Groq(api_key=api_key)
        self.default_model = default_model or "llama-3.1-8b-instant"

    def _request(self, prompt_input: LLMRequest) -> LLMResponse:
        """Execute request to Groq API.

        Args:
            prompt_input: LLMRequest containing the prompt configuration

        Returns:
            LLMResponse with the model's response and token usage
        """
        try:
            # Make the API call
            response = self.client.chat.completions.create(
                model=prompt_input.model or self.default_model,
                messages=[{
                    "role": "system",
                    "content": prompt_input.system_message
                }, {
                    "role": "user",
                    "content": prompt_input.user_message
                }],
                response_format={
                    "type": "json_object"
                }
            )

            # Extract response and token usage
            completion = response.choices[0].message.content
            token_usage = LLMTokenUsage(
                input_token=response.usage.prompt_tokens,
                output_token=response.usage.completion_tokens
            )

            return LLMResponse(
                response_str=completion,
                token_usage=token_usage
            )

        except Exception as e:
            logger.error(f"Error making request to Groq API: {str(e)}")
            raise
