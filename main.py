from src.audio_utils import record_audio, convert_m4a_to_wav
from src.summarization import summarize_with_gpt
from src.transcription import transcribe_audio

def main():
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
        print("For example, if your file is 'Recording.m4a', just type 'Recording.m4a'")
        m4a_file = input("Filename: ")
        wav_file = "converted_audio.wav"
        convert_m4a_to_wav(m4a_file, wav_file)
    else:
        print("Invalid choice. Exiting.")
        exit()
    
    transcribed_text_lt = transcribe_audio(wav_file, language='lt-LT')
    if transcribed_text_lt:
        print("\nTranscribed text:")
        print(transcribed_text_lt)
        
        # Save transcribed text to a Markdown file
        with open("transcribed_text.md", "w", encoding="utf-8") as f:
            f.write(f"# Transcribed Text\n\n{transcribed_text_lt}")

        summary_gpt = summarize_with_gpt(transcribed_text_lt)
        if summary_gpt:
            print("\nSummary:")
            print(summary_gpt)
            
            # Save summary to a Markdown file
            with open("summary.md", "w", encoding="utf-8") as f:
                f.write(f"# Summary\n\n{summary_gpt}")
        else:
            print("\nFailed to generate summary.")
    else:
        print("\nFailed to transcribe audio.")

if __name__ == "__main__":
    main()