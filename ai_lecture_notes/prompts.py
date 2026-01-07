SUMMARY_PROMPT = """
You are an AI teaching assistant.

Convert the following lecture transcript into:
1. A short, clear summary (5–6 lines)
2. Key concepts (bullet points)
3. Exam-oriented notes in simple language

Transcript:
{text}
"""

MCQ_PROMPT = """
You are an AI exam question generator.

Generate {num_questions} {difficulty}-level multiple-choice questions
from the lecture transcript below.

Difficulty rules:
- Easy: Basic definitions, direct facts, simple recall
- Medium: Conceptual understanding, cause-effect, comparisons
- Hard: Analytical, application-based, tricky exam-style questions

Rules:
- Each question must have 4 options (A, B, C, D)
- Clearly mention the correct answer after each question
- Do NOT repeat questions
- Questions must strictly follow the selected difficulty

Transcript:
{text}
"""
