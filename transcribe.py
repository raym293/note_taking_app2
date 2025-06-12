import speech_recognition as sr
from os import path
from pydub import AudioSegment
from pydub.utils import mediainfo
import os

# Helper function to convert any audio file to wav
def convert_to_wav(input_path, output_path="./transcript.wav"):
    info = mediainfo(input_path)
    ext = info["format_name"]
    sound = AudioSegment.from_file(input_path, format=ext)
    sound.export(output_path, format="wav")
    return output_path

def transcribe_first_audio():
    AUDIO_DIR = "audio"
    audio_files = [f for f in os.listdir(AUDIO_DIR) if os.path.isfile(os.path.join(AUDIO_DIR, f))]
    AUDIO_FILE = os.path.join(AUDIO_DIR, audio_files[0]) if audio_files else None

    if AUDIO_FILE:
        # Convert to wav if not already a wav file
        if not AUDIO_FILE.lower().endswith('.wav'):
            wav_file = convert_to_wav(AUDIO_FILE)
            os.remove(AUDIO_FILE)  # Remove the original non-wav file
            AUDIO_FILE = wav_file
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file
            result = r.recognize_google(audio)
        os.remove(AUDIO_FILE)  # Delete the wav file after transcription
        return result
    else:
        return None

if __name__ == "__main__":
    result = transcribe_first_audio()
    if result:
        print("Transcription: " + result)
    else:
        print("No audio files found in the audio directory.")