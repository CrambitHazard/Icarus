# ICARUS ASSISTANT — MASTER PLAN

## Overview
This plan is derived from PRD.md and must be followed for all development. Always refer to this file before making changes or implementing features.

---

## PHASED ROADMAP

| Phase | Goal | Output |
|-------|------|--------|
| 1 | Core voice loop (STT → LLM → TTS) + File reading | MVP voice assistant |
| 2 | File search, edit, and summaries + Tool execution + command confirmation | Functional assistant |
| 3 | Wake-word trigger + Memory + Logging | Persistent voice assistant |
| 4 | Screenshot + OCR + Perplexity integration | Multimodal agent |
| 5 | Web dashboard + plugin system + local fallback LLM | Full Jarvis experience |

---

## PHASE 1: MVP Voice Assistant

### Goals
- Listen to mic input (press-to-talk or timed)
- Convert speech to text (Whisper base, local)
- Send text to OpenRouter LLM for reasoning
- Speak response via OpenVoice
- Read .txt/.md/.pdf files aloud on command
- Log all interactions in timestamped log.json

### Functional Requirements
- `icarus` command or button to start listening
- Mic input via `pyaudio` or `speech_recognition`
- Output via OpenVoice TTS
- File reading and summarization (.txt, .md, .pdf)
- Configurable OpenRouter model

### Folder Structure (Phase 1)
```
icarus-assistant/
├── main.py
├── config/
│   └── openrouter.yaml
├── stt/
│   └── whisper_wrapper.py
├── llm/
│   └── openrouter_client.py
├── tts/
│   └── openvoice_wrapper.py
├── actions/
│   └── read_file.py
├── utils/
│   └── audio_handler.py
├── data/
│   └── logs/
│       └── interaction_log.json
└── README.md
```

### Milestones (Phase 1)
1. Set up Python environment (venv, Whisper, OpenVoice, OpenRouter SDK)
2. Test local STT via Whisper base
3. Connect OpenRouter and get model response
4. Send response to TTS
5. Implement `read_file.py` (with safety checks)
6. Build `main.py` loop
7. Test: "Read me this file" → Icarus speaks output

---

## FUTURE PHASES (Summary)

### Phase 2
- Tool routing, file edits, app control, confirmations
- Add: summarize_pdf.py, search_files.py, edit_text.py, move_files.py, launch_app.py, system_tools.py

### Phase 3
- Wake-word trigger, memory, action logging
- Add: orchestrator/wakeword_listener.py, intent_router.py, task_dispatcher.py, memory_manager.py
- **Memory and context will be implemented using [LangChain](https://python.langchain.com/), [LangGraph](https://langchain-ai.github.io/langgraph/), and a persistent SQLite database (`data/memory.sqlite`).**
- **LangChain will manage conversation history, retrieval, and context passing to the LLM. LangGraph will enable advanced conversational flows and state management.**

### Phase 4
- Screenshot OCR, Perplexity integration
- Add: vision/screenshot.py, ocr_reader.py, web/perplexity_launcher.py

### Phase 5
- GUI dashboard, plugin system, local fallback LLM
- Add: interface/voice_console.py, dashboard_ui.py, plugin system

---

## Implementation Rules
- Always follow this plan and PRD.md
- Use Google-style docstrings
- 4-space indentation, max 100 chars/line
- Kebab-case file naming
- Required folders: ideas/, scratch/, backlog/, tests/
- Test coverage ≥ 80%
- All new features must be added to this plan before implementation

---

## Next Steps
- [x] Implement Phase 2: Functional Assistant
    - Create orchestrator/intent_router.py for tool routing and intent recognition
    - Add actions/search_files.py for file search by name/content/pattern
    - Add utils/confirm.py and utils/path_guard.py for safety confirmations and folder access rules
    - Add actions/launch_app.py for launching applications by name
    - Integrate new tools into main loop via intent router
    - **Add actions/edit_text.py for text file editing**
    - **Add actions/move_files.py for file moving/copying**
    - **Add actions/summarize_pdf.py for PDF summarization**
- [x] Test all new features and update documentation
- [x] Update this plan as new phases or features are started
- [x] Polish Phase 1 & 2 (User Experience, Robustness, and Quality)
    - Add clear, user-friendly error messages for all tools
    - Add a help command or prompt ("help" shows available commands/intents)
    - Add confirmation prompts for potentially destructive actions (edit, move, delete)
    - Ensure all logs are always valid JSON and auto-recover if corrupted
    - Allow dynamic switching between voice/manual modes at any prompt
    - Add a "repeat last response" command
    - Add a "clear log" or "show log" command for user review
    - Improve fuzzy matching for file names (show top 3 matches if ambiguous)
    - Add option to search file contents by default or on demand
    - Add support for more file types (e.g., .docx, .xlsx, .csv) with graceful fallback
    - Add a "list files in directory" command
    - Allow user to select TTS voice, speed, and volume (if supported)
    - Add a "mute"/"unmute" command for TTS
    - Add a "transcribe only" mode for STT (no LLM call)
    - Add more common applications to the launch map (user-editable)
    - Add feedback if an app is not found or fails to launch
    - Add a "list running apps" or "system info" command
    - Add Google-style docstrings to all new/updated functions
    - Add inline comments for complex logic
    - Update README.md with all new features, usage examples, and troubleshooting
    - Ensure all modules pass linting and basic type checks
    - Add test scripts for each tool
    - Add more detailed logging (timestamps, error types, user actions)
    - Add a "test mode" for safe experimentation
- [x] **Phase 2 is now fully complete. All required tools (edit, move, summarize PDF) are implemented and tested.**

### Next steps
- [ ] Review user feedback on new tools and polish as needed
- [ ] Consider adding real API integration for weather/jokes if desired
- [ ] Continue to expand everyday tools based on user needs

---

## PHASE 3: PERSISTENT VOICE ASSISTANT

### Goals
- Wake-word detection ("Icarus") for hands-free operation
- Persistent conversation memory using LangChain and SQLite
- Advanced conversational flows with LangGraph
- Context-aware responses and tool usage
- Session management and state persistence

### Functional Requirements
- Wake-word detection using local speech recognition
- LangChain integration for memory management
- LangGraph for conversational state machines
- SQLite database for persistent storage
- Context-aware tool routing and execution
- Session management with conversation history

### Dependencies
```bash
pip install langchain langgraph sqlite3 speech_recognition pyaudio
```

### 📁 Enhanced Folder Structure (Phase 3)
```
icarus-assistant/
├── main.py
├── config/
│   ├── openrouter.yaml
│   └── preferences.yaml
├── orchestrator/
│   ├── wakeword_listener.py     # "Icarus" detection
│   ├── intent_router.py         # Context-aware intent routing
│   ├── task_dispatcher.py       # Runs matched action
│   ├── memory_manager.py        # LangChain memory integration
│   └── conversation_graph.py    # LangGraph state machine
├── llm/
│   ├── openrouter_client.py     # Updated for LangChain
│   └── langchain_integration.py # LangChain LLM wrapper
├── tts/
│   └── openvoice_wrapper.py
├── stt/
│   └── whisper_wrapper.py
├── actions/
│   ├── read_file.py
│   ├── search_files.py
│   ├── launch_app.py
│   └── system_tools.py
├── utils/
│   ├── audio_handler.py
│   ├── confirm.py
│   └── path_guard.py
├── data/
│   ├── memory.sqlite            # LangChain memory storage
│   └── logs/
│       ├── interaction_log.json
│       └── error_log.json
└── README.md
```

### 🗄️ Database Schema (memory.sqlite)
```sql
-- Conversation sessions
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    session_id TEXT UNIQUE,
    created_at TIMESTAMP,
    last_activity TIMESTAMP,
    context_summary TEXT
);

-- Conversation messages
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    session_id TEXT,
    role TEXT, -- 'user' or 'assistant'
    content TEXT,
    timestamp TIMESTAMP,
    metadata TEXT -- JSON for tool calls, context, etc.
);

-- Tool execution history
CREATE TABLE tool_executions (
    id INTEGER PRIMARY KEY,
    session_id TEXT,
    tool_name TEXT,
    parameters TEXT, -- JSON
    result TEXT,
    timestamp TIMESTAMP,
    success BOOLEAN
);

-- Context embeddings (for retrieval)
CREATE TABLE context_embeddings (
    id INTEGER PRIMARY KEY,
    session_id TEXT,
    content_hash TEXT,
    embedding BLOB,
    timestamp TIMESTAMP
);
```

### 🔧 Implementation Plan

#### 3.1 LangChain Integration
1. **Install Dependencies**
   ```bash
   pip install langchain langgraph sqlite3
   ```
2. **Create LangChain Memory Manager** (`orchestrator/memory_manager.py`)
   - Implement conversation memory using LangChain's `ConversationBufferWindowMemory`
   - SQLite backend for persistent storage
   - Context retrieval and management
   - Session state tracking
3. **Update LLM Client** (`llm/langchain_integration.py`)
   - Wrap OpenRouter with LangChain's `ChatOpenAI`
   - Integrate memory into conversation flow
   - Handle context injection and retrieval

#### 3.2 LangGraph State Machine
1. **Create Conversation Graph** (`orchestrator/conversation_graph.py`)
   - Define conversation states (listening, processing, responding)
   - Implement state transitions and conditions
   - Handle tool execution within conversation flow
   - Manage context switching and memory updates
2. **State Definitions**
   - `LISTENING`: Waiting for wake-word or user input
   - `PROCESSING`: Analyzing intent and routing to tools
   - `RESPONDING`: Generating and speaking response
   - `TOOL_EXECUTION`: Running file operations, app launches, etc.

#### 3.3 Wake-Word Detection
1. **Implement Wake-Word Listener** (`orchestrator/wakeword_listener.py`)
   - Continuous audio monitoring
   - "Icarus" keyword detection using speech recognition
   - Background listening with low CPU usage
   - Seamless transition to conversation mode
2. **Audio Processing**
   - Real-time audio stream analysis
   - Noise reduction and voice activity detection
   - Wake-word confidence scoring

#### 3.4 Enhanced Intent Router
1. **Context-Aware Routing** (`orchestrator/intent_router.py`)
   - Use conversation history for better intent recognition
   - Handle follow-up questions and references
   - Maintain conversation context across tool calls
2. **Memory-Enhanced Intent Detection**
   - Reference previous conversations and actions
   - Handle pronouns and context-dependent queries
   - Provide personalized responses based on history

#### 3.5 Session Management
1. **Session Lifecycle**
   - Automatic session creation on wake-word
   - Session timeout and cleanup
   - Context persistence across sessions
   - Multi-session support for different contexts
2. **Context Management**
   - Conversation summarization for long sessions
   - Context window management
   - Memory retrieval for relevant historical information

### ✅ Milestones (Phase 3)
1. ✅ Set up LangChain and LangGraph dependencies
2. ✅ Implement SQLite database schema and memory storage
3. ✅ Create LangChain memory manager with conversation history
4. ✅ Update LLM client to use LangChain with memory
5. ✅ Implement wake-word detection system
6. ✅ Create LangGraph conversation state machine
7. ✅ Integrate context-aware intent routing
8. ✅ Test persistent conversation with memory
9. ✅ Implement session management and cleanup
10. ✅ Add conversation summarization and context retrieval

### 🧪 Testing Strategy
- **Memory Persistence**: Verify conversation history survives restarts
- **Context Awareness**: Test follow-up questions and references
- **Wake-Word Accuracy**: Measure false positive/negative rates
- **Session Management**: Test session timeouts and context switching
- **Tool Integration**: Ensure tools work within conversation flow
- **Performance**: Monitor memory usage and response times

### 🎯 Success Criteria
- Assistant responds to "Icarus" wake-word reliably
- Conversation history persists across sessions
- Context-aware responses to follow-up questions
- Seamless tool execution within conversation flow
- Session management with automatic cleanup
- Memory retrieval for relevant historical information

---

## FUTURE PHASES (Updated Summary)

### Phase 4
- Screenshot OCR, Perplexity integration
- Add: vision/screenshot.py, ocr_reader.py, web/perplexity_launcher.py
- **Enhanced with LangChain vision capabilities and multimodal memory**

### Phase 5
- GUI dashboard, plugin system, local fallback LLM
- Add: interface/voice_console.py, dashboard_ui.py, plugin system
- **LangGraph-based plugin architecture and dashboard integration**

## [DONE] Full integration of LangChain, LangGraph, and SQLite for memory
- ConversationGraph now uses LangGraph for stateful conversation flows
- Every user and assistant turn is stored in SQLite via MemoryManager
- LangChain ConversationBufferWindowMemory is kept in sync with database
- LLM context is always up to date with full conversation history
- Removed redundant/legacy JSON log in favor of database-backed memory

### Next steps
- [ ] Expand LangGraph state machine for more advanced flows (tool use, error handling, etc.)
- [ ] Add memory search/recall features (e.g., semantic search, summaries)
- [ ] Continue to polish and test persistent memory and context features 