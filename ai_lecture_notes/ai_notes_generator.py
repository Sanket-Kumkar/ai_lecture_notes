import google.generativeai as genai
from prompts import SUMMARY_PROMPT, MCQ_PROMPT

# Configure Gemini
import os
import google.generativeai as genai

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not set")

genai.configure(api_key=api_key)


# Free & stable model
model = genai.GenerativeModel("models/gemini-flash-latest")

def generate_summary(transcript):
    prompt = SUMMARY_PROMPT.format(text=transcript)
    response = model.generate_content(prompt)
    return response.text

def generate_mcqs(transcript, num_questions=10, difficulty="Medium"):
    prompt = MCQ_PROMPT.format(
        text=transcript,
        num_questions=num_questions,
        difficulty=difficulty
    )
    response = model.generate_content(prompt)
    return response.text
