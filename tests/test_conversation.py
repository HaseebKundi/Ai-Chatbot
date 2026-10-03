from chatbot_app.conversation import Conversation


def test_system_prompt_is_first():
    c = Conversation("SYS", 10)
    c.add_user("hi")
    msgs = c.to_api_messages()
    assert msgs[0] == {"role": "system", "content": "SYS"}
    assert msgs[1]["content"] == "hi"


def test_history_is_trimmed_and_starts_with_user():
    c = Conversation("SYS", 4)
    for i in range(5):
        c.add_user(f"u{i}")
        c.add_assistant(f"a{i}")
    msgs = c.to_api_messages()[1:]
    assert len(msgs) <= 4
    assert msgs[0]["role"] == "user"


def test_clear_and_rollback():
    c = Conversation("SYS", 10)
    c.add_user("hi")
    c.rollback_last_user()
    assert len(c) == 0
    c.add_user("a")
    c.add_assistant("b")
    c.clear()
    assert len(c) == 0
