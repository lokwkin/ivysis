from pydantic import BaseModel
from typing import List
from llm.schemas.base import LLMTemplate
from llm.templates.default import DEFAULT_TEMPLATE


class EmailClassifierOutput(BaseModel):
    reasoning: str
    scenarios: List[str]
    # aspects: List[str]
    # score: int


EMAIL_CLASSIFIER = LLMTemplate(
    name="email_classifier",
    system_message=DEFAULT_TEMPLATE.system_message,
    user_message="""You are given the subject and sender of the user's email.
Suggest any likely scenarios in which the user might receive this email. (Could be none or multiple)
Then suggest any aspects of implications about the user that the scenario tells you, possible aspects are: (Could be none or multiple)
- Profession
- Interests
- Location
- Schedule

For example:
Title: Monthly Bank statement from Citibank, UK
Scenarios:
["The user has an bank account with Citibank UK."]

Title: Medium Weekly Digest for Liverpool and Manchester United
Scenarios:
["The user is a football fan and likes Liverpool and Manchester United.", "The user has subscribed to Medium Service.]

Subject: {{subject}}
Sender: {{sender}}

You must return a JSON object with following schema:
{
    "reasoning": str,
    "scenarios": List[str]
}
""",
    output_model=EmailClassifierOutput,
)
