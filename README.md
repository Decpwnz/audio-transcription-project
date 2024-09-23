# Audio Transcription Project

This project aims to transcribe audio files using Python. It provides functionality for recording audio, converting M4A files to WAV, transcribing audio to text, and summarizing the transcribed text using GPT-3.5

## Features

- Record audio directly from the microphone
- Convert M4A audio files to WAV format
- Transcribe audio files to text (supports Lithuanian language)
- Summarize transcribed text using GPT-3.5

## Setup

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Windows (Command Prompt): `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
   - On Git Bash or WSL: `source venv/Scripts/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up your OpenAI API key:
   - Create an account on OpenAI and get your API key
   - Set the environment variable: `export OPENAI_API_KEY='your-api-key-here'`

## Usage

Run the main script:

Follow the prompts to either record new audio or use a pre-recorded M4A file. The script will transcribe the audio and provide a summary.

## Dependencies

- pyaudio
- SpeechRecognition
- pydub
- openai

For a complete list of dependencies, see `requirements.txt`.
