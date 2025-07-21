# Icarus Assistant (MVP)

A lightweight, offline-first, voice-powered personal agent. This MVP implements a core voice loop (STT → LLM → TTS) and basic file reading.

## Features
- Listen to mic input (press-to-talk or timed)
- Convert speech to text (Whisper base, local)
- Send text to OpenRouter LLM for reasoning (via direct API calls)
- Speak response via OpenVoice (manual setup required)
- Read .txt/.md/.pdf files aloud on command
- Log all interactions in timestamped log.json

## Folder Structure
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

## Setup
1. **Create and activate virtual environment**
   ```sh
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Unix/Mac:
   source .venv/bin/activate
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure OpenRouter**
   - Add your API key and model choice to `config/openrouter.yaml`.
   - The assistant uses direct API calls to OpenRouter (see `llm/openrouter_client.py`).
4. **Set up OpenVoice**
   - OpenVoice is not available via pip. You must install and configure it manually.
   - See the official OpenVoice documentation for setup and usage.

## Usage
- Run the assistant:
  ```sh
  python main.py
  ```
- Use the `icarus` command or button to start listening.

## Notes
- **OpenVoice**: Not available on PyPI. Manual setup required. See official docs.
- **OpenRouter**: Accessed via direct API calls using the `requests` library.

## Milestones
See `plan.md` for the full roadmap and implementation plan.
