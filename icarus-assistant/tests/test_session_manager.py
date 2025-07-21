import time
import pytest
from orchestrator.session_manager import SessionManager

class DummyMemory:
    pass

@pytest.fixture
def session_manager():
    return SessionManager(DummyMemory())

def test_create_and_get_session(session_manager):
    session_id = 'sess1'
    session_manager.create_session(session_id, 'TestSession')
    session = session_manager.get_active_session(session_id)
    assert session is not None
    assert session['session_id'] == session_id
    assert session['session_name'] == 'TestSession'

def test_update_session_activity(session_manager):
    session_id = 'sess2'
    session_manager.create_session(session_id)
    old_time = session_manager.get_active_session(session_id)['last_activity']
    time.sleep(0.01)
    session_manager.update_session_activity(session_id)
    new_time = session_manager.get_active_session(session_id)['last_activity']
    assert new_time > old_time

def test_cleanup_expired_sessions(session_manager):
    session_id = 'sess3'
    session_manager.create_session(session_id)
    session_manager.active_sessions[session_id]['last_activity'] -= 1000  # Simulate old session
    session_manager.cleanup_expired_sessions()
    assert session_manager.get_active_session(session_id) is None

def test_list_sessions(session_manager):
    session_manager.create_session('sess4', 'S4')
    session_manager.create_session('sess5', 'S5')
    sessions = session_manager.list_sessions()
    ids = [s['session_id'] for s in sessions]
    assert 'sess4' in ids and 'sess5' in ids

def test_edge_case_duplicate_session(session_manager):
    session_id = 'dupe'
    session_manager.create_session(session_id, 'First')
    session_manager.create_session(session_id, 'Second')  # Should overwrite or ignore
    session = session_manager.get_active_session(session_id)
    assert session['session_id'] == session_id 