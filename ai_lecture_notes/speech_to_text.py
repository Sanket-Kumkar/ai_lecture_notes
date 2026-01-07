import whisper

def transcribe_audio(audio_path):
    model = whisper.load_model("base")  # fast + accurate
    result = model.transcribe(audio_path)
    return result["text"]
