from pydantic import BaseModel

from llm.schemas.base import LLMTemplate


class DefaultResult(BaseModel):
    response: str


DefaultTemplate = LLMTemplate(
    system_message="You are a helpful assistant.",
    user_message="",
    output_model=DefaultResult,
)
