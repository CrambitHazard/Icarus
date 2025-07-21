"""
llm_brain.py

LLMBrain: Advanced intent parsing using OpenRouter LLM as the agent's brain.
"""
from typing import Dict, List, Optional
import json

class LLMBrain:
    """LLM acts as the brain for intent parsing and decision making."""
    def __init__(self, openrouter_client, memory_manager):
        """Initialize LLMBrain with LLM client and memory manager.

        Args:
            openrouter_client: LLM client (OpenRouter).
            memory_manager: Conversation memory manager.
        """
        self.llm = openrouter_client
        self.memory = memory_manager
        self.tools = self._load_tools()
        self.functions = self._load_functions()

    def parse_intent(self, user_query: str, session_id: str) -> Dict:
        """Parse user intent using LLM with full context.

        Args:
            user_query (str): The user's query.
            session_id (str): Conversation session ID.

        Returns:
            Dict: Structured intent/action output from LLM.
        """
        context = self._build_context(session_id)
        prompt = self._create_brain_prompt(user_query, context)
        response = self.llm.query(prompt)
        return self._parse_llm_response(response)

    def _build_context(self, session_id: str) -> Dict:
        """Build context for LLM prompt (history, tools, functions, outputs)."""
        history = self.memory.get_history(session_id)
        return {
            "conversation_history": history[-10:],
            "available_tools": self.tools,
            "available_functions": self.functions,
            "possible_outputs": self._get_possible_outputs(),
            "session_context": self._get_session_context(session_id)
        }

    def _create_brain_prompt(self, user_query: str, context: Dict) -> str:
        """Create detailed prompt for LLM brain."""
        return f"""
You are the brain of Icarus Assistant. You have access to all tools and functions.

CONTEXT:
- Conversation History: {json.dumps(context['conversation_history'], indent=2)}
- Available Tools: {json.dumps(context['available_tools'], indent=2)}
- Available Functions: {json.dumps(context['available_functions'], indent=2)}
- Possible Outputs: {json.dumps(context['possible_outputs'], indent=2)}

USER QUERY: \"{user_query}\"

TASK: Analyze the query and decide what to do. Return a JSON response with:
{{
    "action": "tool_call|function_call|direct_response|plan_mode",
    "target": "tool_name|function_name|response_text|plan_request",
    "parameters": {{...}},
    "confidence": 0.95,
    "reasoning": "Why this action was chosen"
}}

If the query is too complex, set action to "plan_mode".
"""

    def _parse_llm_response(self, response: str) -> Dict:
        """Parse LLM response into structured format."""
        try:
            return json.loads(response)
        except Exception:
            return {
                "action": "direct_response",
                "target": response,
                "parameters": {},
                "confidence": 0.5,
                "reasoning": "Failed to parse structured response"
            }

    def _load_tools(self) -> Dict:
        """Return available tools with descriptions."""
        return {
            "perplexity_search": "Advanced web search using the Perplexity app.",
            "search_files": "Search for files by name, content, or pattern.",
            "read_file": "Read aloud the contents of a file.",
            "edit_text": "Edit the contents of a text file.",
            "move_files": "Move or copy files to a new location.",
            "summarize_pdf": "Summarize the contents of a PDF file.",
            "launch_app": "Launch an application by name.",
            "system_tools": "Access system information and utilities.",
        }

    def _load_functions(self) -> Dict:
        """Return available functions with descriptions."""
        return {
            "get_current_time": "Get the current system time.",
            "get_current_date": "Get the current system date.",
            "get_battery_percentage": "Get the current battery percentage.",
            "get_cpu_usage": "Get the current CPU usage.",
            "get_ram_usage": "Get the current RAM usage.",
            "get_clipboard": "Get the current clipboard contents.",
            "set_clipboard": "Set the clipboard contents.",
            "open_url": "Open a URL in the default browser.",
            "get_weather": "Get the current weather information.",
            "get_random_joke": "Get a random joke.",
        }

    def _get_possible_outputs(self) -> List[str]:
        """Return possible outputs for the agent."""
        return [
            "tool_call",
            "function_call",
            "direct_response",
            "plan_mode",
        ]

    def _get_session_context(self, session_id: str) -> Dict:
        """Return session context (metadata, active tools, etc.)."""
        session_manager = getattr(self.memory, 'session_manager', None)
        if session_manager is not None:
            session = session_manager.get_active_session(session_id)
            return session or {}
        return {} 