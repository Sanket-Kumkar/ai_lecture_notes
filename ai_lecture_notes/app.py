import streamlit as st
import os

from speech_to_text import transcribe_audio
from ai_notes_generator import generate_summary, generate_mcqs
from pdf_generator import generate_pdf

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="AI Lecture Voice-to-Notes Generator",
    layout="centered"
)

st.title("🎧 AI Lecture Voice-to-Notes Generator")
st.write("Upload a lecture audio file and generate AI-powered study notes & MCQs.")

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "transcript" not in st.session_state:
    st.session_state.transcript = None

if "ai_notes" not in st.session_state:
    st.session_state.ai_notes = None

if "mcqs" not in st.session_state:
    st.session_state.mcqs = None

# --------------------------------------------------
# File Upload
# --------------------------------------------------
from assemblyai_utils import upload_file, start_transcription, wait_for_transcription

uploaded_file = st.file_uploader(
    "Upload Lecture Audio / Video",
    type=["wav", "mp3", "m4a", "mp4"]
)

if uploaded_file and st.session_state.transcript is None:
    # Save locally
    with open("temp_media", "wb") as f:
        f.write(uploaded_file.read())

    st.info("📤 Uploading media for transcription...")

    # Upload to AssemblyAI
    media_url = upload_file("temp_media")

    st.info("⏳ Transcription in progress...")

    # Start transcription
    transcript_id = start_transcription(media_url)

    # Wait for the transcription result
    transcript_text = wait_for_transcription(transcript_id)

    st.session_state.transcript = transcript_text
    st.success("✅ Transcription completed!")

    os.remove("temp_media")

# --------------------------------------------------
# Show Transcript
# --------------------------------------------------
if st.session_state.transcript:
    st.subheader("📝 Lecture Transcript")
    st.text_area(
        "Transcript",
        st.session_state.transcript,
        height=300
    )

# --------------------------------------------------
# MCQ Settings
# --------------------------------------------------
if st.session_state.transcript:
    st.subheader("🧪 MCQ Settings")

    difficulty = st.selectbox(
        "Select MCQ Difficulty",
        ["Easy", "Medium", "Hard"],
        index=1
    )

    num_questions = st.selectbox(
        "Number of MCQs",
        [5, 10, 15, 20],
        index=1
    )

    if st.button("🤖 Generate AI Notes"):
        with st.spinner("🧠 Generating AI study material..."):
            st.session_state.ai_notes = generate_summary(
                st.session_state.transcript
            )
            st.session_state.mcqs = generate_mcqs(
                st.session_state.transcript,
                num_questions=num_questions,
                difficulty=difficulty
            )

# --------------------------------------------------
# Display AI Notes
# --------------------------------------------------
if st.session_state.ai_notes:
    st.markdown("### 📌 AI-Generated Summary & Notes")
    st.write(st.session_state.ai_notes)

# --------------------------------------------------
# Display MCQs
# --------------------------------------------------
if st.session_state.mcqs:
    st.markdown("### ❓ Practice MCQs")
    st.write(st.session_state.mcqs)

    # --------------------------------------------------
    # PDF Export
    # --------------------------------------------------
    if st.button("📄 Download PDF"):
        pdf_file = "AI_Lecture_Notes.pdf"
        generate_pdf(
            pdf_file,
            st.session_state.ai_notes,
            st.session_state.mcqs,
            difficulty,
            num_questions
        )

        with open(pdf_file, "rb") as f:
            st.download_button(
                label="⬇️ Click to Download PDF",
                data=f,
                file_name=pdf_file,
                mime="application/pdf"
            )

# --------------------------------------------------
# Reset
# --------------------------------------------------
if st.button("🔄 Upload New Lecture"):
    st.session_state.transcript = None
    st.session_state.ai_notes = None
    st.session_state.mcqs = None
    st.experimental_rerun()

