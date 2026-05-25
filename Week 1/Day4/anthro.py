import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("ANTROPIC-API-KEY")

client = anthropic.Anthropic(api_key=api_key)

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "What should I search for to find the latest developments in renewable energy?",
        }
    ],
)
print(message.content)

