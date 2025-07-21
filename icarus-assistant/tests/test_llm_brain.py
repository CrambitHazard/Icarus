import pytest
from orchestrator.llm_brain import LLMBrain

class DummyLLM:
    def __init__(self, response):
        self._response = response
        self.last_prompt = None
    def query(self, prompt):
        self.last_prompt = prompt
        return self._response

class DummySessionManager:
    def get_active_session(self, session_id):
        return {'session_id': session_id, 'meta': 'test'}

class DummyMemory:
    def get_history(self, session_id):
        return [{'role': 'user', 'content': 'Hi'}, {'role': 'assistant', 'content': 'Hello'}]
    session_manager = DummySessionManager()

def test_parse_intent_direct_response():
    llm = DummyLLM('{"action": "direct_response", "target": "Hello!", "parameters": {}, "confidence": 1.0, "reasoning": "Simple reply"}')
    brain = LLMBrain(llm, DummyMemory())
    result = brain.parse_intent('Hi', 'sess1')
    assert result['action'] == 'direct_response'
    assert result['target'] == 'Hello!'

def test_parse_intent_plan_mode():
    llm = DummyLLM('{"action": "plan_mode", "target": "plan_request", "parameters": {}, "confidence": 1.0, "reasoning": "Complex query"}')
    brain = LLMBrain(llm, DummyMemory())
    result = brain.parse_intent('Do something complex', 'sess2')
    assert result['action'] == 'plan_mode'

def test_parse_intent_malformed_response():
    llm = DummyLLM('not a json')
    brain = LLMBrain(llm, DummyMemory())
    result = brain.parse_intent('Hi', 'sess3')
    assert result['action'] == 'direct_response'
    assert 'not a json' in result['target']

def test_context_includes_tools_and_functions():
    llm = DummyLLM('{}')
    brain = LLMBrain(llm, DummyMemory())
    context = brain._build_context('sess4')
    assert 'available_tools' in context
    assert 'available_functions' in context
    assert isinstance(context['available_tools'], dict)
    assert isinstance(context['available_functions'], dict)

def test_edge_case_empty_history():
    class EmptySessionManager:
        def get_active_session(self, session_id):
            return None
    class EmptyMemory:
        def get_history(self, session_id):
            return []
        session_manager = EmptySessionManager()
    llm = DummyLLM('{}')
    brain = LLMBrain(llm, EmptyMemory())
    context = brain._build_context('sess5')
    assert context['conversation_history'] == [] 