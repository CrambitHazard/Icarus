import pytest
from orchestrator.conversation_graph import ConversationGraph

class DummyLLM:
    def __init__(self, response):
        self._response = response
    def query(self, input_text, session_id=None):
        return self._response

class DummyMemory:
    pass

def test_conversation_graph_basic():
    cg = ConversationGraph(llm=DummyLLM('Hello!'), memory_manager=DummyMemory())
    result = cg.run('Hi', session_id='sess1')
    assert result == 'Hello!'

def test_conversation_graph_no_llm():
    cg = ConversationGraph(llm=None, memory_manager=DummyMemory())
    result = cg.run('Hi', session_id='sess2')
    assert '[No LLM]' in result

def test_conversation_graph_verbose(capsys):
    cg = ConversationGraph(llm=DummyLLM('Hi!'), memory_manager=DummyMemory(), verbose=True)
    cg.run('Test', session_id='sess3')
    captured = capsys.readouterr()
    assert '[ConversationGraph] Running LangGraph' in captured.out 