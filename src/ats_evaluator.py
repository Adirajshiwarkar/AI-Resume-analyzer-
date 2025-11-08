import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_resume_with_ai(resume_text, job_role):
    model = genai.GenerativeModel("gemini-2.5-pro")

    prompt = f"""
    You are an ATS (Applicant Tracking System) evaluation expert.
    Evaluate the resume for the position of {job_role} and provide:
    1. Overall ATS Score (0–100)
    2. Keywords Match Score (0–100)
    3. Formatting Score (0–100)
    4. Structure Score (0–100)
    5. Skills Relevance Score (0–100)
    6. A short summary paragraph (1–2 lines)

    Resume:
    {resume_text}
    """

    response = model.generate_content(prompt)
    text = response.text

    # Extract all numeric scores
    numbers = re.findall(r"\b(\d{1,3})\b", text)
    numbers = [int(n) for n in numbers if 0 <= int(n) <= 100]

    if len(numbers) >= 5:
        sub_scores = {
            "overall": numbers[0],
            "keywords": numbers[1],
            "formatting": numbers[2],
            "structure": numbers[3],
            "skills": numbers[4]
        }
    else:
        sub_scores = {"overall": 0, "keywords": 0, "formatting": 0, "structure": 0, "skills": 0}

    return text, sub_scores
