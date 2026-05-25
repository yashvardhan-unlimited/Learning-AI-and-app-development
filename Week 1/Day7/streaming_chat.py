from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Groq client using OpenAI SDK
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Store conversation history
messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant."
    }
]

print("=" * 60)
print("Groq Streaming Chat CLI")
print("Type 'exit' or 'quit' to stop.")
print("=" * 60)

while True:
    user_input = input("\nYou: ")

    # Exit condition
    if user_input.lower() in ["exit", "quit"]:
        print("\nGoodbye!")
        break

    # Add user message
    messages.append({
        "role": "user",
        "content": user_input
    })

    print("\nAssistant: ", end="", flush=True)

    full_response = ""

    # Streaming response
    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        stream=True
    )

    # Print tokens as they arrive
    for chunk in stream:
        content = chunk.choices[0].delta.content

        if content:
            print(content, end="", flush=True)
            full_response += content

    print()

    # Save assistant response
    messages.append({
        "role": "assistant",
        "content": full_response
    })