"""Configuration: all settings come from environment variables (.env)."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

DEFAULT_MODEL = "openai/gpt-oss-20b"


class ConfigError(Exception):
    """Raised when the configuration is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    api_key: str
    model: str = DEFAULT_MODEL
    temperature: float = 0.7
    max_tokens: int = 1024
    timeout: float = 30.0          # seconds per request
    max_retries: int = 2           # automatic retries on network/5xx/429
    max_history_messages: int = 20  # messages kept as context (user + assistant)
    max_input_chars: int = 2000


def _read(name: str, default, cast):
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return cast(raw)
    except ValueError:
        raise ConfigError(f"{name} in .env must be a valid {cast.__name__}, got '{raw}'.")


def load_settings() -> Settings:
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or api_key.startswith("PASTE_"):
        raise ConfigError(
            "GROQ_API_KEY is missing. Create a .env file (copy .env.example) "
            "and add your key from https://console.groq.com/keys"
        )
    return Settings(
        api_key=api_key,
        model=_read("MODEL", DEFAULT_MODEL, str),
        temperature=_read("TEMPERATURE", 0.7, float),
        max_tokens=_read("MAX_TOKENS", 1024, int),
        timeout=_read("REQUEST_TIMEOUT", 30.0, float),
        max_retries=_read("MAX_RETRIES", 2, int),
        max_history_messages=_read("MAX_HISTORY_MESSAGES", 20, int),
        max_input_chars=_read("MAX_INPUT_CHARS", 2000, int),
    )
