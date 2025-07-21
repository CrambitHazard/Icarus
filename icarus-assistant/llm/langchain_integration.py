"""
langchain_integration.py

LangChain LLM wrapper for OpenRouter with memory/context support.
"""
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import HumanMessage, AIMessage
from typing import Optional
# from langchain.llms import ChatOpenAI  # Uncomment and adapt for OpenRouter

class LangChainLLM:
    """Wraps OpenRouter LLM with LangChain for context-aware chat."""
    def __init__(self, api_key: str, model: str, memory_manager, verbose: bool = False):
        self.api_key = api_key
        self.model = model
        self.memory_manager = memory_manager
        self.memory = ConversationBufferWindowMemory(k=10)
        self.verbose = verbose
        # Placeholder: Replace with actual OpenRouter LLM integration
        # self.llm = ChatOpenAI(api_key=api_key, model=model)

    def query(self, prompt: str, session_id: Optional[str] = None) -> str:
        """Query the LLM with prompt and session context."""
        # Fetch history from memory_manager
        history = self.memory_manager.get_history(session_id) if session_id else []
        messages = []
        for msg in history:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))
        messages.append(HumanMessage(content=prompt))
        if self.verbose:
            print(f"[LangChainLLM] Context for LLM:")
            for m in messages:
                print(f"  - {m}")
        # Store user message in memory
        if session_id:
            self.memory_manager.store_message(session_id, 'user', prompt)
        # Placeholder: Replace with actual LLM call
        # response = self.llm(messages)
        response = "[LLM response placeholder for: {}]".format(prompt)
        # Store assistant response in memory
        if session_id:
            self.memory_manager.store_message(session_id, 'assistant', response)
        return response 