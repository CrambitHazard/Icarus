Here’s the **complete, phase-by-phase product blueprint** for building your offline-first, voice-powered personal agent — **“Icarus”**.

---

# 🧭 PHASED ROADMAP — *ICARUS ASSISTANT*

| Phase       | Goal                                                                     | Output                     |
| ----------- | ------------------------------------------------------------------------ | -------------------------- |
| **Phase 1** | Core voice loop (STT → LLM → TTS) + File reading                         | MVP voice assistant        |
| **Phase 2** | File search, edit, and summaries + Tool execution + command confirmation | Functional assistant       |
| **Phase 3** | Wake-word trigger + Memory + Logging                                     | Persistent voice assistant |
| **Phase 4** | Screenshot + OCR + Perplexity integration                                | Multimodal agent           |
| **Phase 5** | Web dashboard + plugin system + local fallback LLM                       | Full Jarvis experience     |

---

# 📄 PHASE 1 PRD — *ICARUS Voice Assistant (MVP)*

### 🧠 Overview

A lightweight, locally-run assistant that:

* Listens to mic input (press-to-talk or timed)
* Converts speech to text (via Whisper)
* Sends text to OpenRouter LLM for reasoning
* Speaks the response (via OpenVoice)

---

## 🎯 Goals

| Feature      | Spec                                                            |
| ------------ | --------------------------------------------------------------- |
| 🎙️ STT      | Use Whisper (base model, local)                                 |
| 🧠 LLM       | OpenRouter API (Mixtral, Claude, etc.)                          |
| 🗣️ TTS      | OpenVoice (local, realistic voice)                              |
| 📁 File read | User says: “Read this file” → assistant reads .txt or .md aloud |
| 🔁 Flow loop | Trigger → Transcribe → Reason → Speak → Idle                    |
| 📛 Logging   | All inputs/outputs stored in timestamped `log.json`             |

---

## 🧪 Functional Requirements

* `icarus` command or button to start listening
* Mic input recorded via `pyaudio` or `speech_recognition`
* Output spoken via OpenVoice TTS
* Ability to read and summarize `.txt`, `.md`, `.pdf` files on command
* Config to choose OpenRouter default model

---

## 📁 FOLDER STRUCTURE — *Phase 1*

```
icarus-assistant/
├── main.py                      # Main loop
├── config/
│   └── openrouter.yaml          # API key + model choice
├── stt/
│   └── whisper_wrapper.py       # STT using Whisper base
├── llm/
│   └── openrouter_client.py     # LLM caller
├── tts/
│   └── openvoice_wrapper.py     # TTS via OpenVoice
├── actions/
│   └── read_file.py             # Reads and returns .txt/.md
├── utils/
│   └── audio_handler.py         # Mic handling utilities
├── data/
│   └── logs/
│       └── interaction_log.json
└── README.md
```

---

## ✅ Milestones for Phase 1

1. ✅ Set up Python environment (`venv`, Whisper, OpenVoice, OpenRouter SDK)
2. ✅ Test local STT via Whisper base
3. ✅ Connect OpenRouter and get model response
4. ✅ Send response to TTS
5. ✅ Implement `read_file.py` (with safety checks)
6. ✅ Build `main.py` loop
7. ✅ Test sample run: “Read me this file” → Icarus speaks output

---

# 🏗️ FINAL FOLDER STRUCTURE — *ICARUS Full Assistant*

```
icarus/
├── main.py
├── config/
│   ├── openrouter.yaml
│   └── preferences.yaml
├── orchestrator/
│   ├── wakeword_listener.py     # "Icarus" detection
│   ├── intent_router.py         # Determines tool vs LLM
│   ├── task_dispatcher.py       # Runs matched action
│   └── memory_manager.py        # Memory, logs, sessions
├── llm/
│   └── openrouter_client.py
├── tts/
│   └── openvoice_wrapper.py
├── stt/
│   └── whisper_wrapper.py
├── vision/
│   ├── screenshot.py
│   └── ocr_reader.py
├── web/
│   └── perplexity_launcher.py
├── actions/
│   ├── read_file.py
│   ├── summarize_pdf.py
│   ├── search_files.py
│   ├── edit_text.py
│   ├── move_files.py
│   ├── launch_app.py
│   └── system_tools.py
├── utils/
│   ├── logger.py
│   ├── confirm.py               # Safety confirmations
│   ├── path_guard.py            # Folder access rules
│   └── audio_handler.py
├── data/
│   ├── memory.sqlite
│   └── logs/
│       ├── interaction_log.json
│       └── error_log.json
├── interface/
│   ├── voice_console.py         # CLI mic/response viewer
│   └── dashboard_ui.py          # Optional web UI
└── README.md
```

---

# 🧩 Phase Summary Table

| Phase | Key Additions                                        |
| ----- | ---------------------------------------------------- |
| 1     | STT → LLM → TTS, basic file reading                  |
| 2     | Tool routing, file edits, app control, confirmations |
| 3     | Wake-word trigger, memory, action logging            |
| 4     | Screenshot OCR, Perplexity integration               |
| 5     | GUI dashboard, plugin system, local fallback LLM     |

---

# 🧠 Want This Ready on Cursor?

I can now generate:

* A `.cursor.json` task planner
* Cursor-ready folder setup with TODOs as docstrings
* Your `.env` + `openrouter.yaml` scaffolding

Let me know what depth you want next:

* Phase 1 implementation plan (step-by-step per file)?
* Prompt schema examples?
* Tool plugins to prioritize?
