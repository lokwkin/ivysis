from pydantic import BaseModel
from llm.schemas.base import LLMTemplate


class Implication(BaseModel):
    category: str
    description: str


class Email(BaseModel):
    idx: int
    implications: list[Implication]


class PersonaExtractionBatchResult(BaseModel):
    emails: list[Email]


PersonaExtractionBatchPrompt = LLMTemplate(
    system_message="You are a personal secretary of your boss. You are trying to understand your boss's persona from the emails he sent and received.",
    user_message="""You are given the a batch of meta data of emails received or sent by your boss.

For each email, suggest any persona-related information about your boss that can be implied from the emails, under following categories:
Category (scope of the category)
- "background" (Birthplace, family, early education, and foundational influences.)
- "key_milestones" (Significant life events that define a person's journey (e.g., graduation, career breakthroughs, major accomplishments).)
- "cultural_identity" (Nationality, ethnicity, or other cultural affiliations that shape their worldview.)
- "personality" (Innate traits (e.g., introverted, analytical, empathetic).)
- "vision_values" (Life philosophy, ethical beliefs, and guiding principles.)
- "strengths_weaknesses" (Natural abilities or inherent challenges.)
- "interests" (passions or topics that consistently excite them.)
- "specialty" (Primary area of expertise or mastery (e.g., software engineering, public speaking).)
- "profession" (Current profession or occupation.)

Each implication should focus on one single fact.
FYI your boss's email address is {{address}}, use this to determine whether the email is sent or received by your boss.

Some examples of emails and their implications:
Email Subject: Medium Weekly Digest for Liverpool and Manchester United
Implications:
- My boss is a football fan. (interests)

Email Subject: Monthly Bank statement from Citibank, UK
Implications:
- My boss has an bank account with Citibank UK. (background)
- My boss likely lives in the UK. (background)

Email Subject: New restaurants people in Peninsula love
Implications: (None) # Email not likely related to any persona

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
    "emails": [{
        "idx": int, # index of the email in the batch
        "implications": [
            {
                "category": str, # one of the categories provided above
                "description": str # the content of the implication
            }
        ]
    }]
}
</JsonSchema>
""",
    output_model=PersonaExtractionBatchResult,
)


# - "background"
# - "key_milestones"
# - "cultural_identity"
# - "personality"
# - "core_vision_values"
# - "innate_strengths_weaknesses"
# - "core_interests"
# - "current_interests"
# - "core_specialty"
# - "skill_set"
# - "vision_future"
# - "growth_areas"
# - "achievements"
# - "contributions"
# - "desired_legacy"
