import queue
import subprocess
import threading
import time


class VoiceFeedback:
    def __init__(self, cooldown_seconds=1.5):
        self.cooldown_seconds = cooldown_seconds

        self.last_spoken_message = ""
        self.last_spoken_time = 0

        self.message_queue = queue.Queue()

        self.worker_thread = threading.Thread(
            target=self._speech_worker,
            daemon=True,
        )
        self.worker_thread.start()

    def speak(self, message):
        """
        Queue a coaching message to be spoken.

        This avoids repeating the same cue constantly.
        """

        if not message:
            return

        now = time.time()

        same_message = message == self.last_spoken_message
        still_in_cooldown = now - self.last_spoken_time < self.cooldown_seconds

        if same_message and still_in_cooldown:
            return

        print(f"SPEAKING: {message}")

        self.last_spoken_message = message
        self.last_spoken_time = now

        # Clear old messages so the voice coach does not lag behind.
        self._clear_queue()

        self.message_queue.put(message)

    def _clear_queue(self):
        while not self.message_queue.empty():
            try:
                self.message_queue.get_nowait()
            except queue.Empty:
                break

    def _speech_worker(self):
        while True:
            message = self.message_queue.get()
            self._speak_with_windows_voice(message)

    def _speak_with_windows_voice(self, message):
        """
        Uses Windows built-in speech synthesis through PowerShell.

        This is more reliable on Windows than pyttsx3 for this live-camera app.
        """

        powershell_script = """
Add-Type -AssemblyName System.Speech
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speaker.Rate = 1
$text = [Console]::In.ReadToEnd()
$speaker.Speak($text)
"""

        try:
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", powershell_script],
                input=message,
                text=True,
                capture_output=True,
                check=False,
            )
        except Exception as error:
            print(f"Voice feedback error: {error}")