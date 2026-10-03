"""Input validation for user messages."""
from __future__ import annotations


def validate_input(text: str, max_chars: int) -> str:
    """Return the cleaned message or raise ValueError with a friendly reason."""
    cleaned = (text or "").strip()
    if not cleaned:
        raise ValueError("Please type a message.")
    if len(cleaned) > max_chars:
        raise ValueError(
            f"Message is too long ({len(cleaned)} characters). Limit is {max_chars}."
        )
    return cleaned
