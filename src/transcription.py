import speech_recognition as sr

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
    pass