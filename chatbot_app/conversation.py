"""Conversation memory: stores history and keeps it within a size limit."""
from __future__ import annotations


class Conversation:
    def __init__(self, system_prompt: str, max_messages: int = 20):
        self._system = {"role": "system", "content": system_prompt}
        self._max = max(2, max_messages)
        self._messages: list[dict] = []

    def add_user(self, text: str) -> None:
        self._messages.append({"role": "user", "content": text})
        self._trim()

    def add_assistant(self, text: str) -> None:
        self._messages.append({"role": "assistant", "content": text})
        self._trim()

    def rollback_last_user(self) -> None:
        """Remove the last user message (used when the API call fails)."""
        if self._messages and self._messages[-1]["role"] == "user":
            self._messages.pop()

    def clear(self) -> None:
        self._messages.clear()

    def to_api_messages(self) -> list[dict]:
        return [self._system, *self._messages]

    def __len__(self) -> int:
        return len(self._messages)

    def _trim(self) -> None:
        """Keep only the newest messages; history must start with a user turn."""
        if len(self._messages) > self._max:
            self._messages = self._messages[-self._max:]
        while self._messages and self._messages[0]["role"] != "user":
            self._messages.pop(0)
