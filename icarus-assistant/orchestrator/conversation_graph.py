"""
conversation_graph.py

LangGraph state machine for conversation flow.
"""
from typing import Optional, TypedDict
from langgraph.graph import StateGraph, END

class ConversationStateSchema(TypedDict):
    input_text: str
    session_id: str
    llm: object
    memory_manager: object
    response: Optional[str]

def listen(state: dict) -> dict:
    return state

def process(state: dict) -> dict:
    # Optionally add more complex processing here
    return state

def respond(state: dict) -> dict:
    if state['llm']:
        state['response'] = state['llm'].query(state['input_text'], session_id=state['session_id'])
    else:
        state['response'] = f"[No LLM] Echo: {state['input_text']}"
    return state

class ConversationGraph:
    """Manages conversation states and transitions using LangGraph."""
    def __init__(self, llm=None, memory_manager=None, verbose: bool = False):
        self.llm = llm
        self.memory_manager = memory_manager
        self.verbose = verbose
        self.graph = StateGraph(ConversationStateSchema)
        self.graph.add_node('LISTENING', listen)
        self.graph.add_node('PROCESSING', process)
        self.graph.add_node('RESPONDING', respond)
        self.graph.add_edge('LISTENING', 'PROCESSING')
        self.graph.add_edge('PROCESSING', 'RESPONDING')
        self.graph.add_edge('RESPONDING', END)
        self.graph.set_entry_point('LISTENING')
        self.executable_graph = self.graph.compile()

    def run(self, input_text: str, session_id: str = None) -> str:
        state: ConversationStateSchema = {
            'input_text': input_text,
            'session_id': session_id,
            'llm': self.llm,
            'memory_manager': self.memory_manager,
            'response': None,
        }
        if self.verbose:
            print(f"[ConversationGraph] Running LangGraph for input: {input_text}")
        result = self.executable_graph.invoke(state)
        return result.get('response', '[No response]') 