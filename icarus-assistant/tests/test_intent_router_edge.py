import pytest
from orchestrator.intent_router import route_intent

def test_ambiguous_command():
    intents = route_intent('edit or move file')
    assert any(i[0] in ('edit_text', 'move_files') for i in intents)

def test_multiple_commands():
    intents = route_intent('read file.txt and launch notepad')
    assert any(i[0] == 'read_file' for i in intents)
    assert any(i[0] == 'launch_app' for i in intents)

def test_unrecognized_command():
    intents = route_intent('foobar blargh')
    assert intents[-1][0] == 'llm_chat'

def test_mixed_language():
    intents = route_intent("launch notepad y buscar archivo")
    assert any(i[0] == 'launch_app' for i in intents)

def test_long_input():
    text = "launch notepad and " + "a " * 1000
    intents = route_intent(text)
    assert isinstance(intents, list)

def test_special_chars():
    intents = route_intent("launch @notepad$")
    assert any(i[0] == 'launch_app' for i in intents)

def test_no_intent_matched():
    intents = route_intent("gibberishinputthatmeansnothing")
    assert any(i[0] == 'llm_chat' for i in intents)

def test_multiple_verbs():
    intents = route_intent("launch notepad and search for plan.md")
    assert any(i[0] == 'launch_app' for i in intents)
    assert any(i[0] == 'search_files' for i in intents) 