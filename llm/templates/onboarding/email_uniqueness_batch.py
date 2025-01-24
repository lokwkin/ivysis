from pydantic import BaseModel
from llm.schemas.base import LLMTemplate
from llm.templates.default import DefaultTemplate


class EmailUniqueness(BaseModel):
    idx: int
    reasoning: str
    score: int


class EmailUniquenessBatchResult(BaseModel):
    emails: list[EmailUniqueness]


EmailUniquenessPrompt = LLMTemplate(
    system_message=DefaultTemplate.system_message,
    user_message="""
You are given the a batch of meta data of emails received or sent by your boss.

For each email, determine how unique the email is, and give a score from 1 - 5.

[Examples]
A marketing email from some popular online services, it is not unique -- Score = 1
A newsletter about some specific topic, it is rather unique -- Score = 4
A meeting invitation from a colleague, it is very unique -- Score = 5

[Email Batch]
{{#emails}}
Idx: {{{idx}}}
Subject: {{{subject}}}
Date: {{{date}}}
Sender: {{{sender}}}
Recipient: {{{recipient}}}
---
{{/emails}}

You must return a JSON object with following schema:
<JsonSchema>
{
    "emails": [
        {
            "idx": int,
            "reasoning": str,
            "score": int
        }
    ]
}
</JsonSchema>
""",
    output_model=EmailUniquenessBatchResult,
)
