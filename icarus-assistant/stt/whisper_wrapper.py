"""
whisper_wrapper.py

Speech-to-Text (STT) wrapper using Whisper base model.
"""

import whisper

class WhisperSTT:
    """Wrapper for Whisper base model speech-to-text.

    Methods:
        transcribe(audio_path: str) -> str: Transcribes audio to text.
    """
    def __init__(self):
        """Initializes the Whisper model."""
        self.model = whisper.load_model('base')

    def transcribe(self, audio_path: str) -> str:
        """Transcribes audio file to text.

        Args:
            audio_path (str): Path to the audio file.

        Returns:
            str: Transcribed text.
        Raises:
            Exception: If transcription fails.
        """
        try:
            result = self.model.transcribe(audio_path)
            return result['text']
        except Exception as e:
            print(f"Error during transcription: {e}")
            raise
