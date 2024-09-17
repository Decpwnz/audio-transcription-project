import pyaudio
import wave
import re
import os
import speech_recognition as sr
from pydub import AudioSegment
from collections import defaultdict
from openai import OpenAI

# Set up the OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def simple_summarize(text, num_sentences=3):
    # Remove special characters and convert to lowercase
    clean_text = re.sub(r'[^\w\s]', '', text.lower())
    
    # Split text into sentences and words
    sentences = text.split('.')
    words = clean_text.split()
    
    # Calculate word frequencies
    word_freq = defaultdict(int)
    for word in words:
        word_freq[word] += 1
    
    # Score sentences based on word frequency
    sentence_scores = []
    for sentence in sentences:
        score = sum(word_freq[word.lower()] for word in sentence.split() if word.lower() in word_freq)
        sentence_scores.append((sentence, score))
    
    # Sort sentences by score and select top ones
    summary_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:num_sentences]
    
    # Join the top sentences to create the summary
    summary = '. '.join(sentence.strip() for sentence, score in summary_sentences) + '.'
    
    return summary

def summarize_with_gpt(text):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Please summarize the following text concisely:\n\n{text}"}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error in GPT summarization: {e}")
        return None

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

        summary = simple_summarize(transcribed_text_lt)
        print("\nSummary:")
        print(summary)

        summary_gpt = summarize_with_gpt(transcribed_text_lt)
        if summary_gpt:
            print("\nSummary (GPT):")
            print(summary_gpt)
        else:
            print("\nFailed to generate GPT summary.")
