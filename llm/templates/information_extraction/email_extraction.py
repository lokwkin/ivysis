from pydantic import BaseModel
from llm.schemas.base import LLMTemplate


class Extraction(BaseModel):
    details: str


class InformationExtractionResult(BaseModel):
    categories: list[str]
    extractions: list[Extraction]


InformationExtractionPrompt = LLMTemplate(
    system_message="""You are a personal secretary of your boss. You are going to extract and organize information about your boss from the email he sent and received.
Use the following description of your boss to help you determine what your boss concerns about.
[Description]
{{{persona}}}
""",
    user_message="""You are given the content of an email received or sent by your boss.

Extract any task or schedule that can be extracted from the email, under following categories: (category keys and their descriptions)
If it is neither a task-related or schedule-related, ignore it.

1.  hobbies: Activities pursued for fun, relaxation, and personal enjoyment.
2.	interested_topics: Areas of curiosity or learning that captivate attention and spark exploration.
3.	profession: Responsibilities, skill-building, and growth related to career and work life.
4.	physical_wellbeing: Efforts to maintain health, fitness, and overall physical care.
5.	financial: Managing income, expenses, savings, and financial planning.
6.	household: Tasks and responsibilities to maintain and organize the living space.
7.	family: Caring for and nurturing immediate family relationships and responsibilities.
8.	relationships: Building and maintaining connections with significant others or close partners.
9.	friends_social: Interactions, events, and activities to strengthen friendships and social networks.
10.	urgent_matters: Addressing emergencies, crises, or time-sensitive issues requiring immediate attention.

Provide the category that the infomration belongs to.
You can extract multiple information from the email. If no information can be extracted, return an empty list.

You must return a JSON object with following schema:
<JsonSchema>
{
    "categories": [str], # related categories, keys provided above
    "extractions": [{
        "nature": str, # the nature of the information, either "task" / "schedule"
        "details": str # the content of the extraction
        "score_reason": str, # the reason why you think this information is important for your boss
        "score": int # in a range 1 to 5, determine how much your boss is concerned about this information, based on his persona
    }]
}
</JsonSchema>

[Email Details]
Subject: {{{subject}}}
Date: {{{date}}}
Sender: {{{sender}}}
Recipient: {{{recipient}}}
Email Content (In markdown format):
{{{content}}}
""",
    output_model=InformationExtractionResult,
)
