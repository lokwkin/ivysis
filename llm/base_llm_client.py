from abc import abstractmethod
import logging
from colorama import Fore, Style
from typing import Optional, TypeVar
import json
from pydantic import BaseModel
import pystache
import time
from common.logger import get_logger
from llm.schemas.base import LLMRequest, LLMResponse, LLMTemplate
import uuid

from llm.templates.default import DefaultTemplate

logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)

T = TypeVar('T', bound=BaseModel)


class BaseLLMClient():
    """Base class for LLM clients that handles prompting and response parsing.

    This abstract class provides a common interface for different LLM implementations,
    handling template rendering, logging, and response parsing.
    """

    @abstractmethod
    def _request(self, prompt_input: LLMRequest) -> LLMResponse:
        """Send a request to the LLM and get the raw response.

        Args:
            prompt_input (LLMRequest): The formatted request containing user and system messages

        Returns:
            LLMResponse: The raw response from the LLM
        """
        pass

    def prompt(self,
               user_message: Optional[str] = None,
               template: Optional[LLMTemplate[T]] = None,
               template_params: Optional[dict] = None
               ) -> T:
        """Process a prompt through the LLM with optional templating.

        Args:
            user_message (Optional[str]): Direct message to send to LLM if no template is used
            template (Option`al[LLMTemplate]): Template containing system and user message templates
            template_params (Optional[dict]): Parameters to render into the template

        Returns:
            T: Parsed response matching the template's output model

        Raises:
            Exception: If template rendering or response parsing fails
        """
        request_id = str(uuid.uuid4()).split('-')[0]

        if template is not None:
            user_message = pystache.render(template.user_message, template_params)
            system_message = pystache.render(template.system_message, template_params)
            OutputModel = template.output_model
        else:
            user_message = user_message
            system_message = DefaultTemplate.system_message
            OutputModel = DefaultTemplate.output_model

        template_name = template.__class__.__name__ if template is not None else 'N/A'
        try:
            logger.debug(f"{Fore.GREEN}<{request_id}> [{template_name}] System Message: {
                         json.dumps(system_message)}{Style.RESET_ALL}")
            logger.debug(f"{Fore.GREEN}<{request_id}> [{template_name}] User Message: {
                         json.dumps(user_message)}{Style.RESET_ALL}")

            llm_input = LLMRequest(user_message=user_message, system_message=system_message, model='llama3.1')
            ts = time.time()
            llm_response = self._request(llm_input)
            time_used_ms = int((time.time() - ts) * 1000)
            logger.debug(f"{Fore.BLUE}<{request_id}> [{template_name}] Response ({time_used_ms}ms): {
                         str(llm_response.response_str)}{Style.RESET_ALL}")

            response_dict = json.loads(llm_response.response_str)

            logger.debug(f"{Fore.YELLOW}<{request_id}> [{template_name}] Response Parsed:\n{
                json.dumps(response_dict, indent=2)}{Fore.RESET}")

            return OutputModel(**response_dict)

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise e
