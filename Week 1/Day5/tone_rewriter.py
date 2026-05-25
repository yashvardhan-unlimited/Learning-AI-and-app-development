# tone_rewriter.py

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPEN_API_KEY")

# Create OpenAI client
client = OpenAI(api_key=api_key)


def rewrite_tones(paragraph):
    """
    Rewrites a paragraph into:
    - Formal tone
    - Casual tone
    - Persuasive tone
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.8,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert writing assistant.\n"
                    "Your task is to rewrite text in different tones.\n"
                    "Always return clearly labeled sections.\n"
                    "Keep the meaning same while changing tone and style."
                )
            },

            # Few-shot example
            {
                "role": "user",
                "content": "Rewrite this: 'Our product helps people save time.'"
            },
            {
                "role": "assistant",
                "content": (
                    "Formal:\n"
                    "Our product enables individuals to optimize their time efficiently.\n\n"

                    "Casual:\n"
                    "Our product helps people get things done faster.\n\n"

                    "Persuasive:\n"
                    "Stop wasting time — our product helps you accomplish more effortlessly!"
                )
            },

            # Actual user input
            {
                "role": "user",
                "content": (
                    f"Rewrite the following paragraph in 3 tones:\n\n"
                    f"1. Formal\n"
                    f"2. Casual\n"
                    f"3. Persuasive\n\n"
                    f"Paragraph:\n{paragraph}\n\n"
                    f"Output Constraints:\n"
                    f"- Use headings\n"
                    f"- Keep each version concise\n"
                    f"- Preserve the original meaning"
                )
            }
        ]
    )

    return response.choices[0].message.content


def main():
    print("=" * 60)
    print("Tone Rewriter CLI")
    print("=" * 60)

    paragraph = input("\nEnter a paragraph:\n\n")
    print("\nwaiting for model response...\n")
    try:
        result = rewrite_tones(paragraph)

        print("\n" + "=" * 60)
        print("REWRITTEN OUTPUT")
        print("=" * 60)
        print(result)
        print("=" * 60)

    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
