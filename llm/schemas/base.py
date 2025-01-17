from typing import Generic, Type, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class LLMTemplate(BaseModel, Generic[T]):
    name: str
    system_message: str
    user_message: str
    output_model: Type[T]


class LLMRequest(BaseModel):
    system_message: str
    user_message: str
    temperature: float = 0.3
    max_tokens: int = 4096
    model: str = "llama3.1"


class LLMTokenUsage(BaseModel):
    input_token: int
    output_token: int


class LLMResponse(BaseModel):
    response_str: str
    token_usage: LLMTokenUsage
