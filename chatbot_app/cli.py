"""Application loop: wires config, validation, memory, API client and UI together."""
from __future__ import annotations

import logging

from .client import ChatClient, ChatError
from .config import ConfigError, load_settings
from .conversation import Conversation
from .prompts import SYSTEM_PROMPT
from .ui import ChatUI
from .validation import validate_input

EXIT_COMMANDS = {"/exit", "/quit", "exit", "quit"}


def _setup_logging() -> None:
    # Logs go to a file (never message contents or the API key).
    logging.basicConfig(
        filename="chatbot.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def run() -> int:
    _setup_logging()
    ui = ChatUI()

    try:
        settings = load_settings()
    except ConfigError as exc:
        ui.show_error(str(exc))
        return 1

    client = ChatClient(settings)
    convo = Conversation(SYSTEM_PROMPT, settings.max_history_messages)
    ui.banner(settings.model)

    while True:
        try:
            raw = ui.prompt()
        except (EOFError, KeyboardInterrupt):
            ui.info("Goodbye!")
            return 0

        command = raw.strip().lower()
        if command in EXIT_COMMANDS:
            ui.info("Goodbye!")
            return 0
        if command == "/clear":
            convo.clear()
            ui.info("Conversation cleared.")
            continue
        if command == "/help":
            ui.help()
            continue

        try:
            text = validate_input(raw, settings.max_input_chars)
        except ValueError as exc:
            ui.warn(str(exc))
            continue

        convo.add_user(text)
        try:
            with ui.thinking():
                reply = client.complete(convo.to_api_messages())
        except ChatError as exc:
            convo.rollback_last_user()
            ui.show_error(str(exc))
            continue
        except KeyboardInterrupt:
            convo.rollback_last_user()
            ui.info("Request cancelled.")
            continue
        except Exception:  # last-resort safety net: never crash the chat
            logging.getLogger(__name__).exception("Unexpected error")
            convo.rollback_last_user()
            ui.show_error("Something went wrong. Details were saved to chatbot.log.")
            continue

        convo.add_assistant(reply)
        ui.show_reply(reply)
