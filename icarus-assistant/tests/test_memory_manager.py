import os
import tempfile
import pytest
from orchestrator.memory_manager import MemoryManager

@pytest.fixture
def temp_db():
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)
    yield db_path
    os.remove(db_path)

def test_create_and_retrieve_session(temp_db):
    mm = MemoryManager(db_path=temp_db)
    session_id = 'testsession1'
    mm.create_session(session_id, session_name='Test Session')
    sessions = mm.get_history(session_id)
    assert sessions == []

def test_store_and_retrieve_message(temp_db):
    mm = MemoryManager(db_path=temp_db)
    session_id = 'testsession2'
    mm.create_session(session_id)
    mm.store_message(session_id, 'user', 'Hello', {'foo': 'bar'})
    mm.store_message(session_id, 'assistant', 'Hi there', None)
    history = mm.get_history(session_id)
    assert len(history) == 2
    assert history[0]['role'] == 'user'
    assert history[0]['content'] == 'Hello'
    assert history[1]['role'] == 'assistant'
    assert history[1]['content'] == 'Hi there'

def test_session_name_set_and_summary(temp_db):
    mm = MemoryManager(db_path=temp_db)
    session_id = 'testsession3'
    mm.create_session(session_id)
    mm.set_session_name(session_id, 'EdgeCaseSession')
    mm.store_message(session_id, 'user', 'A')
    mm.store_message(session_id, 'assistant', 'B')
    summary = mm.summarize_session(session_id)
    assert 'user: A' in summary
    assert 'assistant: B' in summary

def test_edge_case_empty_session_summary(temp_db):
    mm = MemoryManager(db_path=temp_db)
    session_id = 'emptysession'
    mm.create_session(session_id)
    summary = mm.summarize_session(session_id)
    assert summary == ''

def test_edge_case_long_history(temp_db):
    mm = MemoryManager(db_path=temp_db)
    session_id = 'longsession'
    mm.create_session(session_id)
    for i in range(20):
        mm.store_message(session_id, 'user', f'U{i}')
        mm.store_message(session_id, 'assistant', f'A{i}')
    summary = mm.summarize_session(session_id)
    assert summary.count('user:') <= 10
    assert summary.count('assistant:') <= 10 