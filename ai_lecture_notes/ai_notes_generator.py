import google.generativeai as genai
from prompts import SUMMARY_PROMPT, MCQ_PROMPT

# Configure Gemini
genai.configure(api_key="AIzaSyAB9tUMDK9kz2lRwJ_4ebXdDym8T3A7I-8")

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
