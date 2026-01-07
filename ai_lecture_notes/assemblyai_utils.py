import requests
import time
import os

API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not API_KEY:
    raise RuntimeError("ASSEMBLYAI_API_KEY not set")

HEADERS = {
    "authorization": API_KEY,
    "content-type": "application/json"
}

UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"


def upload_file(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(UPLOAD_ENDPOINT, headers=HEADERS, data=f)
    response.raise_for_status()
    return response.json()["upload_url"]


def start_transcription(audio_url):
    data = {"audio_url": audio_url}
    response = requests.post(TRANSCRIPT_ENDPOINT, json=data, headers=HEADERS)
    response.raise_for_status()
    return response.json()["id"]


def wait_for_transcription(transcript_id):
    while True:
        response = requests.get(f"{TRANSCRIPT_ENDPOINT}/{transcript_id}", headers=HEADERS)
        response.raise_for_status()
        result = response.json()
        if result["status"] == "completed":
            return result["text"]
        elif result["status"] == "error":
            raise RuntimeError("Transcription failed")
        time.sleep(3)
