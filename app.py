import os
from dotenv import load_dotenv
import streamlit as st
from src.resume_parser import extract_resume_text
from src.ats_evaluator import analyze_resume_with_ai
from utlis.helper import extract_score_from_response

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🤖", layout="wide")

# ---------- Neon Green & Black Theme ----------
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background-color: #000000;
            color: #00FF7F;
        }

        h1, h2, h3, h4 {
            color: #00FF7F;
            text-align: center;
        }

        p, label, div, span {
            color: #d1ffd1 !important;
        }

        hr {
            border: 1px solid #00FF7F;
        }

        .circle {
            position: relative;
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: conic-gradient(#00FF7F calc(var(--percent) * 1%), #003300 0%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 25px #00FF7F;
            margin: 0 auto;
        }

        .circle::before {
            content: '';
            position: absolute;
            width: 140px;
            height: 140px;
            background-color: #000000;
            border-radius: 50%;
        }

        .circle span {
            position: relative;
            color: #00FF7F;
            font-size: 2rem;
            font-weight: bold;
            z-index: 1;
        }

        .circle-title {
            text-align: center;
            color: #00FF7F;
            font-weight: bold;
            margin-top: 10px;
            font-size: 18px;
        }

        .desc-container {
            background-color: #000000;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #00FF7F;
            margin-top: 10px;
            color: #d1ffd1;
        }

        .detail-circle {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: conic-gradient(
                #00FF7F var(--keywords),
                #00CC66 var(--formatting),
                #00994D var(--structure),
                #006633 var(--skills)
            );
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            box-shadow: 0 0 25px #00FF7F;
            position: relative;
        }

        .detail-circle::before {
            content: '';
            position: absolute;
            width: 160px;
            height: 160px;
            background-color: #000000;
            border-radius: 50%;
            z-index: 0;
        }

        .detail-text {
            position: absolute;
            text-align: center;
            color: #00FF7F;
            font-size: 0.9rem;
            width: 80%;
            z-index: 1;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<h1>🤖 AI Resume Analyzer</h1>
<p style='text-align:center; font-size:18px;'>Upload your resume and get your ATS score with a detailed Resume Analysis breakdown.</p>
<hr>
""", unsafe_allow_html=True)

# ---------- Job Role Selection ----------
job_role = st.selectbox("🎯 Select Job Role:", [
    "AI/ML Engineer", "Data Analyst", "Software Developer",
    "Business Analyst", "DevOps Engineer", "Cybersecurity Analyst"
])

# ---------- File Upload ----------
uploaded_file = st.file_uploader("📄 Upload Resume (PDF, DOCX, or TXT):", type=["pdf", "docx", "doc", "txt"])

if uploaded_file:
    try:
        with st.spinner("Extracting text..."):
            resume_text = extract_resume_text(uploaded_file)

        with st.spinner("Analyzing your resume..."):
            ai_response, sub_scores = analyze_resume_with_ai(resume_text, job_role)
            score = extract_score_from_response(ai_response)

        # Ensure sub-scores exist
        sub_scores = sub_scores or {}
        keywords = sub_scores.get("keywords", 0)
        formatting = sub_scores.get("formatting", 0)
        structure = sub_scores.get("structure", 0)
        skills = sub_scores.get("skills", 0)

        total = keywords + formatting + structure + skills
        if total == 0:
            total = 1  # avoid zero division

        # Convert percentages for CSS
        k = (keywords / total) * 100
        f = k + (formatting / total) * 100
        s = f + (structure / total) * 100
        sk = s + (skills / total) * 100

        # ---------- Visualization Section ----------
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown(f"""
                <div class="circle" style="--percent:{score}">
                    <span>{score}%</span>
                </div>
                <div class="circle-title">ATS SCORE</div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='circle-title'>DETAILED DESCRIPTION</div>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="detail-circle" 
                     style="--keywords:{k}%; --formatting:{f}%; --structure:{s}%; --skills:{sk}%;">
                    <div class="detail-text">
                        <b>Keywords:</b> {keywords}%<br>
                        <b>Formatting:</b> {formatting}%<br>
                        <b>Structure:</b> {structure}%<br>
                        <b>Skills:</b> {skills}%
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class='desc-container'>
                <h4>📘 What Each Percentage Means:</h4>
                <ul>
                    <li><b>Keywords:</b> Job-related keyword alignment.</li>
                    <li><b>Formatting:</b> Resume layout readability by ATS.</li>
                    <li><b>Structure:</b> Logical flow of content sections.</li>
                    <li><b>Skills:</b> Match between technical & soft skills required for the role.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # ---------- AI Suggestions ----------
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 💡 AI Suggestions for Improvement")
        st.info(ai_response)
        st.success("✅ Analysis Complete!")

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
else:
    st.info("Please upload your resume to begin.")
