import json
import os
from openai import OpenAI
import matplotlib.pyplot as plt
from typing import Dict, Any
from jinja2 import Template
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ========== Step 1: Load Data ==========
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Extract overall metrics + detailed subject/chapter info for prompt context
def extract_metrics_and_details(data):
    overall = {
        "accuracy": data.get("accuracy", 0),
        "total_score": data.get("totalMarkScored", 0),
        "total_questions": data["test"].get("totalQuestions", 0),
        "total_attempted": data.get("totalAttempted", 0),
        "total_correct": data.get("totalCorrect", 0),
        "time_taken_sec": data.get("totalTimeTaken", 0)
    }

    # Extract subject-wise details
    subjects = []
    for s in data.get("subjects", []):
        subjects.append({
            "id": s["subjectId"]["$oid"][-4:],  # last 4 chars as ID
            "accuracy": s.get("accuracy", 0),
            "time_taken": s.get("timeTaken", 0),
            "total_questions": s.get("totalQuestions", 0),
            "total_attempted": s.get("totalAttempted", 0),
            "total_correct": s.get("totalCorrect", 0)
        })

    # (Optional) extract chapter-wise info if available
    # chapters = data.get("chapters", [])  # Extend if JSON has chapters

    return overall, subjects

# ========== Step 2: Generate Prompt ==========

def generate_prompt(overall, subjects):
    # Compose a detailed prompt describing the student's performance
    prompt = f"""
You are an expert educational coach.

A student took a test with the following overall results:
- Total Score: {overall['total_score']} out of {overall['total_questions']}
- Accuracy: {overall['accuracy']}%
- Total Attempted: {overall['total_attempted']}
- Total Correct: {overall['total_correct']}
- Time Taken: {overall['time_taken_sec']} seconds

Subject-wise performance:
"""

    for subj in subjects:
        prompt += f"- Subject {subj['id']}: Accuracy {subj['accuracy']}%, Time Taken {subj['time_taken']}s, Questions Attempted {subj['total_attempted']} out of {subj['total_questions']}, Correct {subj['total_correct']}\n"

    prompt += """
Please provide a detailed, personalized and motivating feedback report including:
1. A personalized encouraging introduction based on performance.
2. Performance breakdown emphasizing strong and weak areas.
3. Insightful time vs accuracy analysis.
4. 2-3 actionable, practical suggestions to improve.
Make sure the feedback sounds human and supportive.
"""

    return prompt.strip()

# ========== Step 3: Call OpenAI GPT API ==========

def call_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # use GPT-4-turbo if available, else gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing detailed student performance feedback."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ OpenAI API Error:", e)
        return "⚠️ Failed to generate feedback from OpenAI."

# ========== Step 4: Plot Accuracy Chart ==========

def plot_accuracy(subjects, out_path):
    try:
        subject_ids = [s["id"] for s in subjects]
        accuracies = [s["accuracy"] for s in subjects]

        plt.figure(figsize=(8, 4))
        plt.bar(subject_ids, accuracies, color='skyblue')
        plt.title("Accuracy by Subject")
        plt.xlabel("Subject ID")
        plt.ylabel("Accuracy (%)")
        plt.ylim(0, 100)
        plt.tight_layout()

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        plt.savefig(out_path)
        plt.close()
    except Exception as e:
        print("❌ Failed to plot accuracy graph:", e)

# ========== Step 5: Create Styled PDF ==========
def create_pdf(content, pdf_path, image_path=None):
    try:
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        margin = 50
        current_y = height - margin

        # Title
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(colors.darkblue)
        c.drawString(margin, current_y, "Student Performance Report")
        current_y -= 40

        # Line
        c.setStrokeColor(colors.darkblue)
        c.setLineWidth(1)
        c.line(margin, current_y, width - margin, current_y)
        current_y -= 30

        # Feedback header
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.black)
        c.drawString(margin, current_y, "AI Generated Feedback:")
        current_y -= 25

        # Feedback text
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)

        for line in content.split('\n'):
            max_width = width - 2 * margin
            text_width = c.stringWidth(line, "Helvetica", 12)
            if text_width < max_width:
                c.drawString(margin, current_y, line.strip())
                current_y -= 18
            else:
                # Wrap long lines
                words = line.strip().split()
                line_buffer = ""
                for word in words:
                    if c.stringWidth(line_buffer + word + " ", "Helvetica", 12) < max_width:
                        line_buffer += word + " "
                    else:
                        c.drawString(margin, current_y, line_buffer.strip())
                        current_y -= 18
                        line_buffer = word + " "
                if line_buffer:
                    c.drawString(margin, current_y, line_buffer.strip())
                    current_y -= 18
        current_y -= 20

        # Insert chart image
        if image_path and os.path.exists(image_path):
            img_width = width - 2 * margin
            img_height = img_width * 0.5

            if current_y - img_height < margin:
                c.showPage()
                current_y = height - margin

            c.drawImage(ImageReader(image_path), margin, current_y - img_height, width=img_width, height=img_height)
            current_y -= (img_height + 20)

        # Footer
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.gray)
        c.drawRightString(width - margin, margin / 2, "Generated by AI Feedback System")

        c.save()
        print(f"✅ PDF generated: {pdf_path}")

    except Exception as e:
        print("❌ PDF Generation Error:", e)

# ========== Main Execution ==========
if __name__ == "__main__":
    print("🚀 Starting AI Feedback Report Generation...\n")

    # Load and validate data
    data_list = load_data('data/sample_submission.json')

    if not isinstance(data_list, list) or not data_list:
        print("❌ Error: sample_submission.json should be a non-empty list.")
        exit(1)

    # Extract metrics from the first student's data
    data = data_list[0]

    overall_metrics, subjects = extract_metrics_and_details(data)

    print("📊 Extracted Metrics:")
    print(overall_metrics)
    print("📊 Subject Details:")
    print(subjects)

    prompt = generate_prompt(overall_metrics, subjects)
    print("📨 Prompt ready. Sending to OpenAI...")

    ai_response = call_openai(prompt)
    print("🤖 AI Response received.")

    plot_accuracy(subjects, "report/accuracy.png")
    create_pdf(ai_response, "report/output.pdf", "report/accuracy.png")

    print("\n✅ All done! Check the 'report/' folder.")

