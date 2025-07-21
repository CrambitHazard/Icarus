# Icarus: Offline-First Voice-Powered Personal Agent

## Overview
Icarus is a lightweight, offline-first, voice-powered personal agent designed to run locally and respect your privacy. It features a modular, phase-based roadmap, evolving from a simple voice assistant to a full Jarvis-like experience. Icarus leverages state-of-the-art open-source tools for speech-to-text (STT), large language model (LLM) reasoning, and text-to-speech (TTS), with persistent memory and advanced tool integrations.

---

## 🚀 Phased Roadmap
| Phase | Goal | Output |
|-------|------|--------|
| 1 | Core voice loop (STT → LLM → TTS) + File reading | MVP voice assistant |
| 2 | File search, edit, summaries, tool execution, confirmations | Functional assistant |
| 3 | Wake-word trigger, memory, logging | Persistent voice assistant |
| 4 | Screenshot, OCR, Perplexity integration | Multimodal agent |
| 5 | Web dashboard, plugin system, local fallback LLM | Full Jarvis experience |

See [PRD.md](PRD.md) and [plan.md](plan.md) for full details and milestones.

---

## ✨ Features
- Listen to mic input (press-to-talk or wake-word)
- Convert speech to text (Whisper, local)
- LLM reasoning via OpenRouter API (Mixtral, Claude, etc.)
- Speak responses via OpenVoice (local, realistic TTS)
- Read and summarize `.txt`, `.md`, `.pdf` files aloud
- File search, edit, move, and app launching (Phase 2+)
- Persistent memory and context (LangChain, SQLite, Phase 3+)
- Logging of all interactions
- Modular tool/plugin system (future phases)

---

## 📁 Folder Structure (Phase 3+)
```
icarus-assistant/
├── main.py
├── config/
│   ├── openrouter.yaml
│   └── preferences.yaml
├── orchestrator/
│   ├── wakeword_listener.py
│   ├── intent_router.py
│   ├── plan_executor.py
│   ├── memory_manager.py
│   ├── conversation_graph.py
│   └── session_manager.py
├── llm/
│   ├── openrouter_client.py
│   └── langchain_integration.py
├── tts/
│   └── openvoice_wrapper.py
├── stt/
│   └── whisper_wrapper.py
├── actions/
│   ├── read_file.py
│   ├── summarize_pdf.py
│   ├── search_files.py
│   ├── edit_text.py
│   ├── move_files.py
│   ├── launch_app.py
│   └── system_tools.py
├── utils/
│   ├── audio_handler.py
│   ├── confirm.py
│   ├── path_guard.py
│   └── logger.py
├── data/
│   ├── memory.sqlite
│   └── logs/
│       ├── interaction_log.json
│       └── error_log.json
├── interface/
│   ├── voice_console.py
│   └── dashboard_ui.py
├── ideas/
├── backlog/
├── scratch/
├── tests/
└── README.md
```

---

## 🛠️ Setup
1. **Clone the repo and enter the directory**
   ```sh
   git clone <repo-url>
   cd Icarus/icarus-assistant
   ```
2. **Create and activate a virtual environment**
   ```sh
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Unix/Mac:
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure OpenRouter**
   - Add your API key and model choice to `config/openrouter.yaml` (see example in file).
5. **Set up OpenVoice**
   - OpenVoice is not available via pip. You must install and configure it manually.
   - See the official OpenVoice documentation for setup and usage.

---

## ▶️ Usage
- Run the assistant:
  ```sh
  python main.py
  ```
- Use the `icarus` command or button to start listening (press-to-talk or wake-word, depending on phase).
- For advanced features, see [plan.md](plan.md) and [PRD.md](PRD.md).

---

## ⚙️ Configuration
- **OpenRouter**: Set your model and API key in `config/openrouter.yaml`.
- **OpenVoice**: Manual install required. See [OpenVoice docs](https://github.com/myshell-ai/OpenVoice).
- **Preferences**: (Phase 3+) Edit `config/preferences.yaml` for advanced options.

---

## 📝 Notes
- **OpenVoice**: Not available on PyPI. Manual setup required.
- **OpenRouter**: Accessed via direct API calls using the `requests` library.
- **Memory**: Persistent conversation memory and context are enabled in Phase 3+ (LangChain, SQLite).
- **Testing**: All modules are covered by tests in `tests/` (≥80% coverage required). Run with `pytest`.
- **Required folders**: `ideas/`, `scratch/`, `backlog/`, `tests/` (see [plan.md](plan.md)).

---

## 🧑‍💻 Contributing
- Please read [plan.md](plan.md) and [PRD.md](PRD.md) before contributing.
- All new features must be added to the plan before implementation.
- Use Google-style docstrings, 4-space indentation, max 100 chars/line, and kebab-case file naming.
- Ensure all modules pass linting and type checks.
- Add or update tests for all new features.

---

## 📚 Documentation & Roadmap
- [PRD.md](PRD.md): Product requirements and phased vision
- [plan.md](plan.md): Implementation plan, milestones, and next steps
- [TODO.md](TODO.md): Current tasks and feature backlog

---

## 🧩 Next Steps
See the "Next Steps" section in [plan.md](plan.md) for current priorities and ongoing work.

