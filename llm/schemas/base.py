from typing import Generic, Optional, Type, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class LLMTemplate(BaseModel, Generic[T]):
    system_message: str
    user_message: str
    output_model: Type[T]


class LLMRequest(BaseModel):
    system_message: str
    user_message: str
    temperature: float = 0.3
    max_tokens: int = 4096
    model: Optional[str] = None


class LLMTokenUsage(BaseModel):
    input_token: int
    output_token: int


class LLMResponse(BaseModel):
    response_str: str
    token_usage: LLMTokenUsage
