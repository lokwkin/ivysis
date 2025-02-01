from pydantic import BaseModel
from llm.schemas.base import LLMTemplate


class EmailSummarizingResult(BaseModel):
    summary: str


EmailSummarizingPrompt = LLMTemplate(
    system_message="""You are a personal secretary of your boss. You are going to summarize emails that your boss has received or sent.""",
    user_message="""You are given the content of an email received or sent by your boss.

- Think step by step and reason through the task.
- Summarize the email into a detailed note.
    - Pay attention to your boss's persona provided below and think of what information your boss would concern about from this email, and make sure to include all of them in the summary.
    - Keep the concrete informative or actionables of your boss in the summary. Make sure to include the date, time, location, and other critical descriptive information if provided.
    - Output the summary in text form. Use a fact-based style.
    - Do not hallucinate. Include only details from the email.

You must return a JSON object with following schema:
<JsonSchema>
{
    "thought": str,
    "summary": str
}

[Email Details]
Subject: {{{subject}}}
Date: {{{date}}}
Sender: {{{sender}}}
Recipient: {{{recipient}}}
Email Content (In markdown format):
{{{content}}}

[Boss Persona]
{{{persona}}}
""",
    output_model=EmailSummarizingResult,
)
