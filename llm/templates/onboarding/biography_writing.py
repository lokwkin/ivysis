from pydantic import BaseModel
from llm.schemas.base import LLMTemplate


class BiographyWritingResult(BaseModel):
    biography: str

    class Config:
        extra = 'allow'


BiographyWritingPrompt = LLMTemplate(
    system_message="You are a personal secretary of your boss. You are trying to understand your boss background and personality from the emails he sent and received.",
    user_message="""From the following descriptions of your boss by categories, rewrite it into a text biography of your boss.
If you don't know your boss's name, reference with "My boss".

You must return a JSON object with following schema:
<JsonSchema>
{
    "biography": str # A detailed text biography of your boss
}
</JsonSchema>

[Draft]
{{{draft}}}
""",
    output_model=BiographyWritingResult,
)
