from pydantic import BaseModel
from typing import Optional, List
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json

# Schema for structured output ================================
class Task(BaseModel):
    person: str
    task: str
    deadline: Optional[str] = None


class Meeting(BaseModel):
    event: str
    time: str


class NotesOutput(BaseModel):
    tasks: List[Task]
    meetings: List[Meeting]
# =============================================================


load_dotenv()
OPENAI_API_KEY=os.getenv("OPEN_API_KEY")


with open("sample_notes.txt", "r") as file:
    notes = file.read()



prompt = f"""
Extract all tasks and meetings from these notes.

Return ONLY valid JSON.

Format:
{{
  "tasks": [
    {{
      "person": "...",
      "task": "...",
      "deadline": "..."
    }}
  ],
  "meetings": [
    {{
      "event": "...",
      "time": "..."
    }}
  ]
}}

Notes:
{notes}
"""


# OpenAI version of the code ========================================================================
print("Processing notes with OpenAI...")
client = OpenAI(api_key=OPENAI_API_KEY)
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You extract structured information from notes."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

content = response.choices[0].message.content

data = json.loads(content)

validated = NotesOutput(**data)

print(validated.model_dump_json(indent=2))
# ====================================================================================================

print("=" * 40)


# Anthropic version of the code =====================================================================
print("Processing notes with Anthropic...")
client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)



response = client.messages.create(
    model="claude-3-5-sonnet-latest",
    max_tokens=1024,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

content = response.content[0].text

data = json.loads(content)

validated = NotesOutput(**data)

print(validated.model_dump_json(indent=2))

# ====================================================================================================

