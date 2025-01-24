from pydantic import BaseModel
from llm.schemas.base import LLMTemplate


class Implication(BaseModel):
    category: str
    description: str


class PersonaExtractionResult(BaseModel):
    implications: list[Implication]


PersonaExtractionPrompt = LLMTemplate(
    system_message="You are a personal secretary of your boss. You are trying to understand your boss background and personality from the emails he sent and received.",
    user_message="""You are given the meta data of an email received by your boss.

Suggest any information about your boss (the receiver) that can be implied from the email, under following categories:
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

[Examples]
Email Subject: Medium Weekly Digest for Liverpool and Manchester United
{
    "implications": [
        {
            "category": "interests",
            "description": "My boss is a football fan."
        }
    ]
}

Email Subject: Monthly Bank statement from Citibank, UK
{
    "implications": [
        {
            "category": "background",
            "description": "My boss has an bank account with Citibank UK."
        },
        {
            "category": "background",
            "description": "My boss likely lives in the UK."
        }
    ]
}

Email Subject: New restaurants people in Peninsula love
{
    "implications": []  # Not likely related to boss
}

[Email]
Subject: {{subject}}
Date: {{date}}
From: {{sender}}
To: {{to}}
Cc: {{cc}}

You must return a JSON object with following schema:
<JsonSchema>
{
    "implications": [
        {
            "category": str,
            "description": str
        }
    ]
}
</JsonSchema>
""",
    output_model=PersonaExtractionResult,
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
