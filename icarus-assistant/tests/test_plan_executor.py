import pytest
from orchestrator.plan_executor import PlanExecutor

class DummyLLM:
    def __init__(self, response):
        self._response = response
    def query(self, prompt):
        return self._response

class DummyBrain:
    def _build_context(self, session_id):
        return {'conversation_history': [], 'available_tools': {}, 'available_functions': {}, 'possible_outputs': [], 'session_context': {}}

def test_create_and_execute_plan_sequential():
    plan_json = '{"steps": [{"step_id": 1, "description": "Step 1", "action": "tool_call", "target": "search_files", "parameters": {"query": "foo"}, "parallel": false, "depends_on": []}, {"step_id": 2, "description": "Step 2", "action": "tool_call", "target": "read_file", "parameters": {"file": "bar.txt"}, "parallel": false, "depends_on": [1]}], "parallel_groups": [[1], [2]]}'
    pe = PlanExecutor(DummyBrain(), DummyLLM(plan_json))
    result = pe.create_and_execute_plan('Do X then Y', 'sess1')
    assert 'Step 1' in result and 'Step 2' in result

def test_create_and_execute_plan_parallel():
    plan_json = '{"steps": [{"step_id": 1, "description": "A", "action": "tool_call", "target": "t1", "parameters": {}, "parallel": true, "depends_on": []}, {"step_id": 2, "description": "B", "action": "tool_call", "target": "t2", "parameters": {}, "parallel": true, "depends_on": []}], "parallel_groups": [[1,2]]}'
    pe = PlanExecutor(DummyBrain(), DummyLLM(plan_json))
    result = pe.create_and_execute_plan('Do A and B', 'sess2')
    assert 'Step 1' in result and 'Step 2' in result

def test_aggregate_results_empty():
    pe = PlanExecutor(DummyBrain(), DummyLLM('{}'))
    summary = pe._aggregate_results([])
    assert summary == ''

def test_execute_plan_malformed():
    pe = PlanExecutor(DummyBrain(), DummyLLM('{}'))
    # Plan with missing steps/parallel_groups
    plan = {'steps': [], 'parallel_groups': []}
    results = pe._execute_plan(plan, 'sess3')
    assert results == [] 