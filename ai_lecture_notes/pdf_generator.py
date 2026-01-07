from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import re

def clean_text(text):
    """
    Completely removes tables and converts their content
    into clean bullet points for PDF rendering.
    """

    lines = text.split("\n")
    cleaned_lines = []

    inside_table = False

    for line in lines:
        line = line.strip()

        # Skip empty lines safely
        if not line:
            cleaned_lines.append("")
            continue

        # Detect markdown table rows
        if "|" in line:
            inside_table = True

            # Extract table cells
            cells = [cell.strip() for cell in line.split("|") if cell.strip()]

            # Ignore separator rows like ------
            if all(set(cell) <= {"-", ":"} for cell in cells):
                continue

            # Convert table row to bullet point
            if len(cells) >= 2:
                bullet = "• " + " : ".join(cells)
            else:
                bullet = "• " + cells[0]

            cleaned_lines.append(bullet)
            continue

        # Exit table when normal text resumes
        if inside_table and "|" not in line:
            inside_table = False

        # Remove markdown headers
        if line.startswith("#"):
            cleaned_lines.append(line.replace("#", "").strip())
            continue

        # Clean bullet symbols
        line = line.replace("**", "")
        line = line.replace("* ", "• ")
        line = line.replace("- ", "• ")

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)




def generate_pdf(filename, summary, mcqs, difficulty, num_questions):
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("<b>AI Generated Lecture Notes</b>", styles["Title"]))
    story.append(Spacer(1, 0.3 * inch))

    # Metadata
    story.append(Paragraph(
        f"<b>MCQ Difficulty:</b> {difficulty}<br/>"
        f"<b>Total MCQs:</b> {num_questions}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 0.3 * inch))

    # Clean AI outputs
    summary = clean_text(summary)
    mcqs = clean_text(mcqs)

    # Summary Section
    story.append(Paragraph("<b>Summary & Notes</b>", styles["Heading2"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(summary.replace("\n", "<br/>"), styles["Normal"]))
    story.append(Spacer(1, 0.4 * inch))

    # MCQ Section
    story.append(Paragraph("<b>Multiple Choice Questions</b>", styles["Heading2"]))
    story.append(Spacer(1, 0.2 * inch))

    for line in mcqs.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 0.1 * inch))

    # Build PDF
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    doc.build(story)
