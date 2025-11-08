from setuptools import setup, find_packages

setup(
    name="ai_resume_analyzer",
    version="1.0.0",
    author="Adiraj Shiwarkar",
    description="AI Resume Analyzer with ATS scoring and improvement suggestions.",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "google-generativeai",
        "python-docx",
        "PyPDF2",
        "python-dotenv"
    ],
)
