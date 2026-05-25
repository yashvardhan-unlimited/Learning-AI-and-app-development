from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPEN_API_KEY")


client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-5.5",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)