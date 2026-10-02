import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise SystemExit("Missing GROQ_API_KEY. Create a .env file (see .env.example).")

client = Groq(api_key=api_key)
MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")


def ask_ai(message: str) -> str:
    """Send one user message to the AI model and return its reply."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": message}],
    )
    return response.choices[0].message.content


def main():
    print("AI Chatbot (type 'quit' to exit)\n")
    while True:
        user_message = input("You: ").strip()
        if user_message.lower() in {"quit", "exit"}:
            break
        if not user_message:
            continue
        print("AI:", ask_ai(user_message), "\n")


if __name__ == "__main__":
    main()
