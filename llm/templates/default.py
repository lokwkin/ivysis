from pydantic import BaseModel

from llm.schemas.base import LLMTemplate


class DefaultOutput(BaseModel):
    response: str


DEFAULT_TEMPLATE = LLMTemplate(
    name="default",
    system_message="You are a helpful assistant.",
    user_message="",
    output_model=DefaultOutput,
)
