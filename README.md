# Nova - AI Chatbot (Groq)

A terminal AI chatbot with a defined personality ("Nova", a friendly mentor for
beginners), conversation memory, a loading spinner, Markdown rendering, input
validation and production-style error handling.

## Features
**Day 2**
- User input -> AI response, via the Groq API
- System prompt defining role, style and rules (`chatbot_app/prompts.py`)
- Loading state (spinner while waiting for the model)
- Error handling for invalid key, retired model, rate limits, timeouts, no internet
- Clean terminal interface (panels, colors)

**Day 3 improvements**
- Conversation history / context memory (limited to the last N messages)
- `/clear` command to reset the conversation
- Input validation (empty or too-long messages)
- Markdown rendering of AI answers (code blocks, lists, bold)
- Better prompt structure (Role / Style / Rules sections)

**Production-oriented extras**
- Modular code, one responsibility per file
- All settings in `.env` (model, timeout, retries, history size, limits)
- Automatic retries and request timeout
- Failed requests roll back the history so the chat stays consistent
- Logging to `chatbot.log` (never logs messages or the API key)
- Unit tests with pytest

## Technology used
Python 3.10+, Groq API (`groq` SDK), `python-dotenv`, `rich`, `pytest`

## Project structure
```
ai-chatbot/
├── chatbot.py              # entry point
├── chatbot_app/
│   ├── cli.py              # main loop, commands, wires everything together
│   ├── client.py           # ONLY file that calls the API; maps errors to friendly messages
│   ├── conversation.py     # history/memory, trimming, clear, rollback
│   ├── config.py           # settings loaded from .env
│   ├── prompts.py          # system prompt
│   ├── validation.py       # input validation
│   └── ui.py               # terminal UI (spinner, markdown, panels)
├── tests/                  # pytest unit tests
├── requirements.txt
├── requirements-dev.txt
├── .env.example
└── .gitignore
```

## Architecture
```
 You ──> ui.prompt() ──> validation ──> Conversation (history + system prompt)
                                              │
                                              ▼
 ui.show_reply() <── ChatClient (Groq API, retries, timeout, error mapping)
```
1. `cli.py` reads input and handles commands (`/clear`, `/help`, `/exit`).
2. `validation.py` rejects empty or too-long messages.
3. `conversation.py` adds the message and builds `[system prompt + recent history]`.
4. `client.py` sends it to Groq. Any API failure becomes a friendly `ChatError`.
5. On success the reply is stored in history and rendered as Markdown.
   On failure the user message is rolled back, so history never gets corrupted.

## How to run
```bash
git clone <your-repo-url>
cd ai-chatbot
pip install -r requirements.txt
copy .env.example .env      # Windows   (Mac/Linux: cp .env.example .env)
```
Edit `.env` and set `GROQ_API_KEY` (free key: https://console.groq.com/keys), then:
```bash
python chatbot.py
```
Commands: `/clear` new conversation, `/help`, `/exit`.

Run the tests:
```bash
pip install -r requirements-dev.txt
pytest
```

## Screenshots
![Chat demo](screenshot.png)

## What I learned
- How chat APIs work: a list of messages with `system`, `user`, `assistant` roles
- The model has no memory; the app must resend the history every time
- Why history must be trimmed (token limits, cost, speed)
- Separating code into modules makes it easier to test and change
- Never commit secrets; use `.env` + `.gitignore`

## Problems and solutions
| Problem | Solution |
|---|---|
| API returned `404 model_not_found` because the model was retired | Model name is now configurable via `MODEL` in `.env`, and the error message explains how to fix it |
| App crashed on network/API errors | All API errors are caught in `client.py` and shown as friendly messages |
| A failed request left an unanswered message in history | History rolls back the last user message on failure |
| History grows forever | History is trimmed to the last `MAX_HISTORY_MESSAGES` messages |
| Risk of leaking the API key | Key lives in `.env`, which is in `.gitignore`; logs never contain it |

## What I would improve next
- Streaming responses (show text as it is generated)
- Save/load conversations to a file
- Web UI (Streamlit or FastAPI + React)
- Token-based history limit instead of message count
