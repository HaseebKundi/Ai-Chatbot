# Basic AI Chatbot

## What I built
A simple command-line chatbot. The user types a message, the program sends it
to an AI model on Groq, receives the reply, and prints it in the terminal.

## Technology used
- Python 3
- Groq API (free tier) via the official `groq` SDK, model `llama-3.3-70b-versatile`
- `python-dotenv` for loading the API key from a `.env` file

## How to run
1. Get a free API key at https://console.groq.com/keys
2. Clone the repo and enter the folder:
   ```bash
   git clone <your-repo-url>
   cd ai-chatbot
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create your `.env` file from the example and add your key:
   ```bash
   cp .env.example .env
   # then edit .env and set GROQ_API_KEY=...
   ```
5. Start the chatbot:
   ```bash
   python chatbot.py
   ```
6. Type a message and press Enter. Type `quit` to exit.

## API integration approach
1. The API key is read from `.env` (never committed; `.env` is in `.gitignore`).
2. `ask_ai()` calls `client.chat.completions.create()` with the model and the
   user's message as a single `user` turn.
3. The text in `response.choices[0].message.content` is returned and printed.

## How it works (short explanation)
`input()` reads the user's message -> `ask_ai()` sends it to the Groq API ->
the API returns a response -> `print()` displays it. This repeats in a loop
until the user types `quit`.

## What I learned
- How to call an AI model from code using an SDK
- How to keep secrets out of Git with `.env` and `.gitignore`
- The structure of a chat API request (model, messages) and response (choices)

## What I would improve next
- Add conversation history so the bot remembers earlier messages
- Add error handling for network/API failures
- Add a system prompt and a simple web UI
