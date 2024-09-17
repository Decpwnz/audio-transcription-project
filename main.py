import pyaudio
import wave
import speech_recognition as sr
from pydub import AudioSegment
import os

def record_audio(filename, duration=5, sample_rate=44100, chunk=1024):
    audio = pyaudio.PyAudio()
    
    # Open stream
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)
    
    print("Recording...")
    
    frames = []
    for _ in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    print("Finished recording.")
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Save the recorded data as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

def transcribe_audio(audio_file, language='en-US'):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language=language)
        return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from speech recognition service; {e}")

def convert_m4a_to_wav(m4a_file, wav_file):
    audio = AudioSegment.from_file(m4a_file, format="m4a")
    audio.export(wav_file, format="wav")

if __name__ == "__main__":
    print("Audio Transcription Tool")
    print("1. Record new audio")
    print("2. Use pre-recorded file")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        output_file = "recorded_audio.wav"
        duration = int(input("Enter recording duration in seconds: "))
        record_audio(output_file, duration)
        wav_file = output_file
    elif choice == "2":
        print("Enter the filename of your M4A file (located in the same folder as main.py):")
        print("For example, if your file is 'recording.m4a', just type 'recording.m4a'")
        m4a_file = input("Filename: ")
        wav_file = "converted_audio.wav"
        convert_m4a_to_wav(m4a_file, wav_file)
    else:
        print("Invalid choice. Exiting.")
        exit()
    
    # Transcribe in Lithuanian
    transcribed_text_lt = transcribe_audio(wav_file, language='lt-LT')
    if transcribed_text_lt:
        print("\nTranscribed text (Lithuanian):")
        print(transcribed_text_lt)
