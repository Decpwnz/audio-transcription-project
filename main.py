import pyaudio
import wave
import speech_recognition as sr

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

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from speech recognition service; {e}")

if __name__ == "__main__":
    audio_file = "output.wav"
    record_audio(audio_file, duration=5)
    
    transcribed_text = transcribe_audio(audio_file)
    if transcribed_text:
        print("Transcribed text:")
        print(transcribed_text)
