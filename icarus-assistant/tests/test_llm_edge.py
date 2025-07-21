import pytest
from llm.openrouter_client import OpenRouterClient
import requests
from llm.langchain_integration import LangChainLLM
from orchestrator.memory_manager import MemoryManager
import uuid

@pytest.fixture
def llm():
    return OpenRouterClient(api_key="invalid", model="test-model")

def test_invalid_api_key(llm, monkeypatch):
    def fake_post(*a, **k):
        class R:
            status_code = 401
            def raise_for_status(self): raise requests.HTTPError("401 Unauthorized")
            def json(self): return {}
            text = "Unauthorized"
        return R()
    monkeypatch.setattr(requests, "post", fake_post)
    with pytest.raises(Exception):
        llm.query("test")

def test_network_error(llm, monkeypatch):
    monkeypatch.setattr(requests, "post", lambda *a, **k: (_ for _ in ()).throw(requests.ConnectionError))
    with pytest.raises(Exception):
        llm.query("test")

def test_malformed_response(llm, monkeypatch):
    class R:
        status_code = 200
        def raise_for_status(self): pass
        def json(self): return {"bad": "data"}
        text = "ok"
    monkeypatch.setattr(requests, "post", lambda *a, **k: R())
    with pytest.raises(Exception):
        llm.query("test")

def test_langchainllm_context_memory(tmp_path):
    # Use a temp SQLite DB
    db_path = str(tmp_path / 'memory.sqlite')
    memory = MemoryManager(db_path=db_path)
    llm = LangChainLLM(api_key='dummy', model='dummy', memory_manager=memory)
    session_id = str(uuid.uuid4())
    # Simulate a conversation
    user1 = "Hello, who are you?"
    resp1 = llm.query(user1, session_id=session_id)
    user2 = "What did I just say?"
    resp2 = llm.query(user2, session_id=session_id)
    # Check that both user and assistant messages are stored
    history = memory.get_history(session_id)
    assert any(user1 in m['content'] for m in history)
    assert any(user2 in m['content'] for m in history)
    assert any('LLM response placeholder' in m['content'] for m in history)
    # Check that context is used (placeholder response for now)
    assert resp2.startswith('[LLM response placeholder') 