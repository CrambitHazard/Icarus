"""
conversation_graph.py

Simplified conversation flow manager without LangGraph dependency.
"""
from typing import Optional

class ConversationGraph:
    """Manages conversation states and transitions without LangGraph."""
    def __init__(self, llm=None, memory_manager=None, verbose: bool = False):
        self.llm = llm
        self.memory_manager = memory_manager
        self.verbose = verbose

    def run(self, input_text: str, session_id: str = None) -> str:
        """Simple conversation flow: process input and return response."""
        if self.verbose:
            print(f"[ConversationGraph] Processing input: {input_text}")
        
        # Simple flow: input -> LLM -> response
        if self.llm:
            response = self.llm.query(input_text, session_id=session_id)
        else:
            response = f"[No LLM] Echo: {input_text}"
        
        if self.verbose:
            print(f"[ConversationGraph] Response: {response}")
        
        return response 