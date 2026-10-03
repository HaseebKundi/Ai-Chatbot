import pytest

from chatbot_app.validation import validate_input


def test_valid_message_is_stripped():
    assert validate_input("  hello  ", 100) == "hello"


@pytest.mark.parametrize("bad", ["", "   ", None])
def test_empty_rejected(bad):
    with pytest.raises(ValueError):
        validate_input(bad, 100)


def test_too_long_rejected():
    with pytest.raises(ValueError):
        validate_input("x" * 101, 100)
