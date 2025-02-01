from typing import Literal
from pydantic import BaseModel
from llm.schemas.base import LLMTemplate


class Extraction(BaseModel):
    type: Literal["actionable", "informative"]
    categories: list[str]
    details: str


class InformationExtractionResult(BaseModel):
    extractions: list[Extraction]


InformationExtractionPrompt = LLMTemplate(
    system_message="""You are a personal secretary of your boss. You are going to extract and organize information about your boss from the email he sent and received.""",
    user_message="""You are given the summary of an email received or sent by your boss.

- From the summary provided, extract the actionable or informative items explicitly mentioned in the email.
    - Pay attention to your boss's persona provided below and think of how it is related to your boss.
    - You may extract multiple information from the email. If no information can be extracted, return an empty list.
- For each extractions, identify if it is under any (or multiple) of the following category keys and their descriptions:
    - "hobbies": Activities pursued for fun, relaxation, and personal enjoyment.
    - "interested_topics": Areas of curiosity or learning that draw attention.
    - "profession": Related to career and work life.
    - "physical_wellbeing": Related to personal health, fitness, and overall physical care.
    - "financial": Personal income, expenses, savings, and financial planning.
    - "household": Maintenance of the living space.
    - "family": Immediate family relationships and responsibilities.
    - "relationships": Connections with close partners.
    - "friends_social": Interactions and activities of friendships and social networks.
- Provide a detailed description of the extraction. Include the date, time, location, and other critical details.

Note:
- You should group similar extractions together into a single extraction with details that include all the details.
- Do not hallucinate. Include only details from the email.

You must return a JSON object with following schema:
<JsonSchema>
{
    "extractions": [{
        "type": "actionable" | "informative",
        "categories": [str], # related categories, keys provided above
        "details": str, # A self-contained text description of the extraction
    }]
}
</JsonSchema>

[Email Details]
Subject: {{{subject}}}
Date: {{{date}}}
Sender: {{{sender}}}
Recipient: {{{recipient}}}
Email Summary:
{{{summary}}}

[Boss Persona]
{{{persona}}}
""",
    output_model=InformationExtractionResult,
)
