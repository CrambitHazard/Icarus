"""
plan_executor.py

PlanExecutor: Hierarchical task planning and execution using LLM.
"""
from typing import List, Dict
import json
import threading

class PlanExecutor:
    """Executes complex tasks using hierarchical planning."""
    def __init__(self, llm_brain, openrouter_client):
        """Initialize PlanExecutor with LLM brain and client."""
        self.brain = llm_brain
        self.llm = openrouter_client

    def create_and_execute_plan(self, complex_query: str, session_id: str) -> str:
        """Create a plan for complex queries and execute it.

        Args:
            complex_query (str): The user's complex query.
            session_id (str): Conversation session ID.

        Returns:
            str: Aggregated results from plan execution.
        """
        plan = self._generate_plan(complex_query, session_id)
        results = self._execute_plan(plan, session_id)
        return self._aggregate_results(results)

    def _generate_plan(self, query: str, session_id: str) -> Dict:
        """Generate step-by-step plan for complex query using LLM."""
        context = self.brain._build_context(session_id)
        plan_prompt = f"""
You are a task planner. The user has a complex request: \"{query}\"

CONTEXT: {json.dumps(context, indent=2)}

Create a detailed step-by-step plan. For each step, specify:
- Whether it can be executed in parallel with other steps
- The exact tool/function to use
- Required parameters

Return JSON format:
{{
    "steps": [
        {{
            "step_id": 1,
            "description": "What this step does",
            "action": "tool_call|function_call",
            "target": "tool_name|function_name",
            "parameters": {{...}},
            "parallel": false,
            "depends_on": []
        }}
    ],
    "parallel_groups": [[1, 2], [3], [4, 5]]
}}
"""
        response = self.llm.query(plan_prompt)
        return json.loads(response)

    def _execute_plan(self, plan: Dict, session_id: str) -> List[Dict]:
        """Execute plan steps sequentially or in parallel.

        Args:
            plan (Dict): The plan dictionary with steps and parallel groups.
            session_id (str): Conversation session ID.

        Returns:
            List[Dict]: List of step results.
        """
        steps = {step['step_id']: step for step in plan.get('steps', [])}
        results = {}

        def run_step(step):
            # Stub: Replace with actual tool/function dispatch
            result = {
                'step_id': step['step_id'],
                'description': step['description'],
                'action': step['action'],
                'target': step['target'],
                'parameters': step['parameters'],
                'output': f"Executed {step['action']}:{step['target']} with {step['parameters']}"
            }
            return result

        for group in plan.get('parallel_groups', []):
            threads = []
            group_results = [None] * len(group)
            def make_thread(idx, step_id):
                def target():
                    group_results[idx] = run_step(steps[step_id])
                return threading.Thread(target=target)
            for idx, step_id in enumerate(group):
                t = make_thread(idx, step_id)
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            for idx, step_id in enumerate(group):
                results[step_id] = group_results[idx]
        # Return results in step order
        return [results[step['step_id']] for step in plan.get('steps', []) if step['step_id'] in results]

    def _aggregate_results(self, results: List[Dict]) -> str:
        """Aggregate results from plan execution.

        Args:
            results (List[Dict]): List of step results.

        Returns:
            str: Aggregated summary of results.
        """
        summary = []
        for res in results:
            summary.append(f"Step {res['step_id']}: {res['description']}\nOutput: {res['output']}")
        return "\n---\n".join(summary) 