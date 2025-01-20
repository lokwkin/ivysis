from pydantic import BaseModel
from llm.schemas.base import LLMTemplate
from llm.templates.default import DEFAULT_TEMPLATE


class EmailUniqueness(BaseModel):
    reasoning: str
    score: int


EMAIL_UNIQUENESS = LLMTemplate(
    name="email_uniqueness",
    system_message=DEFAULT_TEMPLATE.system_message,
    user_message="""
You are given the subject, date and sender address of an email received by your boss.

Determine how unique the email is, and give a score from 1 - 5.

[Examples]
A marketing email from some popular online services, it is not unique -- Score = 1
A newsletter about some specific topic, it is rather unique -- Score = 4
A meeting invitation from a colleague, it is very unique -- Score = 5

Subject: {{subject}}
Date: {{date}}
Sender: {{sender}}

You must return a JSON object with following schema:
<JsonSchema>
{
    "reasoning": str,
    "score": int
}
</JsonSchema>
""",
    output_model=EmailUniqueness,
)
