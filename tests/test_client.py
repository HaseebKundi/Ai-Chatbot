from types import SimpleNamespace

import pytest

from chatbot_app.client import ChatClient, ChatError
from chatbot_app.config import Settings


def make_client(content):
    client = ChatClient(Settings(api_key="test-key"))
    reply = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))])
    client._client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **kw: reply))
    )
    return client


def test_returns_reply_text():
    assert make_client(" Hello! ").complete([{"role": "user", "content": "hi"}]) == "Hello!"


def test_empty_reply_raises_friendly_error():
    with pytest.raises(ChatError):
        make_client("").complete([{"role": "user", "content": "hi"}])
