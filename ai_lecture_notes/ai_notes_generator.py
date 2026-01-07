import google.generativeai as genai
from prompts import SUMMARY_PROMPT, MCQ_PROMPT

# Configure Gemini
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


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

