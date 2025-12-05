Whisper (local) setup

This project supports using a local, free Whisper model (via the `openai-whisper` Python package) for audio transcription.

Requirements:
- Python package: openai-whisper (already added to `requirements.txt`)
- system dependency: ffmpeg (must be installed and available in PATH)

Installation (Windows PowerShell):

1) Install ffmpeg (choco recommended):
   choco install ffmpeg -y

2) Install Python deps:
   cd backend
   pip install -r requirements.txt

Configuration:
- Optionally, choose model size with environment variable `WHISPER_MODEL` (e.g. tiny, base, small, medium, large). Default: `small`.

Notes:
- Loading larger models requires more RAM/CPU. Use `tiny`/`base`/`small` for lightweight environments.
- The transcription endpoint will return `{"text": <transcribed text>}` on success or `{"error": "..."}` on failure.
