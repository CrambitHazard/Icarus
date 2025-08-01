"""
langchain_integration.py

Simplified LLM wrapper for OpenRouter with memory/context support.
"""
from typing import Optional

class LangChainLLM:
    """Wraps OpenRouter LLM with memory support."""
    def __init__(self, api_key: str, model: str, memory_manager, verbose: bool = False):
        self.api_key = api_key
        self.model = model
        self.memory_manager = memory_manager
        self.verbose = verbose

    def query(self, prompt: str, session_id: Optional[str] = None) -> str:
        """Query the LLM with prompt and session context."""
        # Fetch history from memory_manager
        history = self.memory_manager.get_history(session_id) if session_id else []
        
        # Build context from history
        context = ""
        if history:
            context = self.memory_manager.get_context_window(session_id, max_messages=10)
            context += "\n\n"
        
        full_prompt = context + "User: " + prompt + "\nAssistant:"
        
        if self.verbose:
            print(f"[LangChainLLM] Context for LLM:")
            print(f"  - Context: {context}")
            print(f"  - Prompt: {prompt}")
        
        # Store user message in memory
        if session_id:
            self.memory_manager.store_message(session_id, 'user', prompt)
        
        # Placeholder: Replace with actual LLM call
        # For now, return a simple response
        response = f"[LLM response placeholder for: {prompt}]"
        
        # Store assistant response in memory
        if session_id:
            self.memory_manager.store_message(session_id, 'assistant', response)
        
        return response 