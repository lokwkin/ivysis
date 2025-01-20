from pydantic import BaseModel
from llm.schemas.base import LLMTemplate


class BiographyFormation(BaseModel):
    description: str

    class Config:
        extra = 'allow'


BIOGRAPHY_FORMATION = LLMTemplate(
    name="biography_formation",
    system_message="You are a personal secretary of your boss. You are trying to understand your boss background and personality from the emails he sent and received.",
    user_message="""You have a list of hypoethesis about your boss, with a weight from 1 to 5 at the end of each indication how important you think the hypothesis is.

Write a description about your boss in string form. The description should be detailed enough so you can use as reference later-on.

Gather the most occuring hypoethesis and those with the highest weight, those are likely to be true.
Opt-out the unlikely hypotheses if there is any contradiction.

You must return a JSON object with following schema:
<JsonSchema>
{
    "likely_hypotheses": str,   # Your thoughts on what significant information you have gathered
    "contradictions": str,  # Your thoughts on any contradiction you found
    "description": str
}
</JsonSchema>

[Hypothesis]
{{#implications}} {{description}} ({{weight}})
{{/implications}}
""",
    output_model=BiographyFormation,
)
