"""
audio_handler.py

Audio handling utilities for microphone input and audio file management.
"""

import pyaudio
import wave
import os
import time

class AudioHandler:
    """Handles microphone input and audio file operations.

    Methods:
        record(duration: int) -> str: Records audio and saves to file.
    """
    def __init__(self):
        """Initializes the audio handler."""
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024
        self.audio = pyaudio.PyAudio()
        self.output_dir = 'scratch'  # Save temp audio files here
        if not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir)
            except PermissionError as e:
                print(f"[AudioHandler] Permission denied creating output_dir: {e}")
                raise

    def record(self, duration: int) -> str:
        """Records audio from the microphone.

        Args:
            duration (int): Duration to record in seconds.

        Returns:
            str: Path to the recorded audio file (WAV).
        Raises:
            Exception: If recording fails.
        """
        if duration <= 0:
            raise ValueError("Duration must be positive")
        timestamp = int(time.time())
        filename = f"audio_{timestamp}.wav"
        filepath = os.path.join(self.output_dir, filename)
        try:
            stream = self.audio.open(format=self.format,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.chunk)
            print(f"[AudioHandler] Recording for {duration} seconds...")
            frames = []
            for _ in range(0, int(self.rate / self.chunk * duration)):
                data = stream.read(self.chunk)
                frames.append(data)
            print("[AudioHandler] Recording complete.")
            stream.stop_stream()
            stream.close()
            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(frames))
            print(f"[AudioHandler] Audio file created: {filepath}")
            # Retain only the 5 most recent audio files
            audio_files = [f for f in os.listdir(self.output_dir) if f.startswith('audio_') and f.endswith('.wav')]
            audio_files.sort(reverse=True)  # Newest first
            for old_file in audio_files[5:]:
                try:
                    os.remove(os.path.join(self.output_dir, old_file))
                except Exception as e:
                    print(f"[AudioHandler] Could not delete old audio file {old_file}: {e}")
            return filepath
        except PermissionError as e:
            print(f"[AudioHandler] Permission denied during recording: {e}")
            raise
        except Exception as e:
            print(f"[AudioHandler] Error during recording: {e}")
            raise
