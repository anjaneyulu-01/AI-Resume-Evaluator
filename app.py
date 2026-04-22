import json
import joblib
import pandas as pd
import streamlit as st
from pathlib import Path

try:
    import PyPDF2
    _PDF_SUPPORT = True
except ImportError:
    _PDF_SUPPORT = False

from utils.logic import (
    extract_resume_info,
    calculate_ats_score,
    get_recommendations,
    get_score_category,
)

st.set_page_config(
    page_title="Resume ATS Score Checker",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .main { padding: 0rem; }
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 20px; border-radius: 15px; text-align: center;
        color: white; margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 { font-size: 2.5em; margin-bottom: 10px; font-weight: 800; }
    .main-header p { font-size: 1.1em; opacity: 0.95; }
    .score-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 30px; border-radius: 20px; text-align: center;
        color: white; margin: 30px 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    .score-label { font-size: 16px; font-weight: 600; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }
    .score-number { font-size: 72px; font-weight: 900; margin: 15px 0; text-shadow: 0 4px 8px rgba(0,0,0,0.2); }
    .score-rating { font-size: 24px; font-weight: 700; margin-top: 10px; }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px; border-radius: 15px; color: white; text-align: center;
        box-shadow: 0 5px 15px rgba(245, 87, 108, 0.3);
    }
    .metric-value { font-size: 32px; font-weight: 800; margin: 10px 0; }
    .metric-label { font-size: 13px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; }
    .progress-container { background: #e9ecef; height: 10px; border-radius: 10px; overflow: hidden; margin: 10px 0; }
    .progress-bar { height: 100%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; transition: width 0.4s ease; }
    .skill-tag {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 8px 15px; border-radius: 20px;
        font-size: 13px; font-weight: 600; display: inline-block; margin: 5px 5px 5px 0;
    }
    .skill-tag-alt {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white; padding: 8px 15px; border-radius: 20px;
        font-size: 13px; font-weight: 600; display: inline-block; margin: 5px 5px 5px 0;
    }
    .recommendation-item {
        background: white; border-left: 4px solid #667eea;
        padding: 20px; margin: 15px 0; border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .recommendation-priority {
        display: inline-block; background: #667eea; color: white;
        padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 700; margin-bottom: 8px;
    }
    .section-header {
        font-size: 22px; font-weight: 700; margin: 30px 0 20px 0;
        padding-bottom: 12px; border-bottom: 3px solid #667eea; display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_models():
    model_dir = Path("model")
    try:
        ats_model = joblib.load(model_dir / "ats_model.pkl")
    except Exception:
        ats_model = None

    try:
        scaler = joblib.load(model_dir / "scaler.pkl")
    except Exception:
        scaler = None

    try:
        with open(model_dir / "model_metadata.json", "r") as f:
            metadata = json.load(f)
    except Exception:
        metadata = {"model_type": "Fallback", "test_r2_score": 0}

    return ats_model, scaler, metadata


def main():
    st.markdown("""
        <div class="main-header">
            <h1>📄 Resume ATS Score Checker</h1>
            <p>AI-powered optimization for Applicant Tracking Systems</p>
        </div>
    """, unsafe_allow_html=True)

    model, scaler, metadata = load_models()

    with st.sidebar:
        st.markdown("### ⚙️ Settings & Info")
        st.markdown("---")
        st.markdown("#### 📊 Model Information")
        st.info(f"""
        **Model Type:** {metadata.get('model_type', 'Unknown')}

        **Accuracy:** {metadata.get('test_r2_score', 0)*100:.1f}%

        **Training:** {metadata.get('training_samples', 'Unknown')} samples
        """)
        st.markdown("---")
        st.markdown("#### 💡 How It Works")
        st.markdown("""
        This tool analyzes your resume:

        - **ATS Score** (0-100)
        - **Skill Detection** (150+ keywords)
        - **Missing Elements**
        - **Smart Recommendations**
        """)
        st.markdown("---")
        st.markdown("#### 📚 What is ATS?")
        st.caption("99% of Fortune 500 companies use ATS. Higher score = better chance of being reviewed!")

    st.markdown("### 📥 Upload Your Resume")
    input_method = st.radio("Choose input method:", ["Paste Text", "Upload File"], horizontal=True)

    resume_text = ""

    if input_method == "Paste Text":
        resume_text = st.text_area(
            "Paste your resume text:",
            height=400,
            placeholder="Paste your complete resume here...",
            label_visibility="collapsed",
        )
    else:
        uploaded_file = st.file_uploader("Upload resume file:", type=["txt", "pdf"])
        if uploaded_file is not None:
            if uploaded_file.type == "text/plain":
                try:
                    resume_text = uploaded_file.read().decode("utf-8")
                except Exception:
                    st.error("Could not read the text file. Please check encoding.")
            elif uploaded_file.type == "application/pdf":
                if not _PDF_SUPPORT:
                    st.error("PDF support unavailable. Please paste your resume as text.")
                else:
                    try:
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        pages_text = [page.extract_text() or "" for page in pdf_reader.pages]
                        resume_text = "".join(pages_text).strip()
                        if not resume_text:
                            st.warning("PDF appears to be image-based or empty. Try pasting text instead.")
                    except Exception:
                        st.error("PDF parsing error. Try pasting text instead.")

    col_btn1, _ = st.columns([1, 1])
    with col_btn1:
        analyze_button = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)

    if analyze_button:
        if not resume_text or not resume_text.strip():
            st.error("❌ Please provide resume text to analyze.")
        else:
            with st.spinner("🔍 Analyzing your resume..."):
                resume_info = extract_resume_info(resume_text)
                score = calculate_ats_score(resume_info, model, scaler)
                category, _ = get_score_category(score)

                st.markdown(f"""
                    <div class="score-container">
                        <div class="score-label">Your ATS Score</div>
                        <div class="score-number">{score:.1f}</div>
                        <div class="score-rating">{category}</div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {score}%"></div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("### 📊 Resume Metrics")
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">🛠️ Skills</div><div class="metric-value">{len(resume_info["skills"])}</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">🎓 Education</div><div class="metric-value">{len(resume_info["education"])}</div></div>', unsafe_allow_html=True)
                with m3:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">🏆 Certs</div><div class="metric-value">{len(resume_info["certifications"])}</div></div>', unsafe_allow_html=True)
                with m4:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">📝 Words</div><div class="metric-value">{resume_info["word_count"]}</div></div>', unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("### 🎯 Detected Content")
                det_col1, det_col2 = st.columns(2)

                with det_col1:
                    st.markdown("#### ✅ Contact Information")
                    if resume_info['email']:
                        st.success(f"✓ Email: {resume_info['email']}")
                    else:
                        st.error("✗ No email found")
                    if resume_info['phone']:
                        st.success(f"✓ Phone: {resume_info['phone']}")
                    else:
                        st.error("✗ No phone found")

                with det_col2:
                    st.markdown("#### 🔍 Skills Found")
                    if resume_info['skills']:
                        st.markdown(f"**Total: {len(resume_info['skills'])} skills**")
                        skill_html = "".join(f'<span class="skill-tag">{s}</span>' for s in resume_info['skills'][:12])
                        st.markdown(skill_html, unsafe_allow_html=True)
                        if len(resume_info['skills']) > 12:
                            st.caption(f"... and {len(resume_info['skills']) - 12} more")
                    else:
                        st.warning("No skills detected. Add technical keywords!")

                st.markdown("---")
                exp_col1, exp_col2 = st.columns(2)

                with exp_col1:
                    st.markdown("#### 🎓 Education")
                    if resume_info['education']:
                        st.markdown("".join(f'<span class="skill-tag-alt">{e}</span>' for e in resume_info['education']), unsafe_allow_html=True)
                    else:
                        st.info("Add your educational background for better scoring")

                with exp_col2:
                    st.markdown("#### 🏆 Certifications")
                    if resume_info['certifications']:
                        st.markdown("".join(f'<span class="skill-tag-alt">{c}</span>' for c in resume_info['certifications']), unsafe_allow_html=True)
                    else:
                        st.info("Professional certifications boost your score")

                st.markdown("---")
                st.markdown("### 💡 Personalized Recommendations")
                recs = get_recommendations(resume_info, score)

                if recs:
                    for rec in recs:
                        priority_color = {'CRITICAL': '#dc3545', 'HIGH': '#fd7e14', 'MEDIUM': '#ffc107', 'LOW': '#17a2b8'}.get(rec['priority'], '#6c757d')
                        st.markdown(f"""
                            <div class="recommendation-item">
                                <div style="color: {priority_color};">
                                    <span class="recommendation-priority">{rec['priority']}</span>
                                </div>
                                <h4 style="margin: 10px 0 5px 0;">{rec['emoji']} {rec['title']}</h4>
                                <p style="margin: 0; font-size: 14px; color: #666;">{rec['detail']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ No recommendations - Your resume is excellent!")

                st.markdown("---")
                st.markdown("### 📈 Detailed Breakdown")
                breakdown_data = {
                    'Component': ['Skills Count', 'Education', 'Certifications', 'Word Count', 'Email', 'Phone'],
                    'Status': [
                        f"{len(resume_info['skills'])} detected",
                        f"{len(resume_info['education'])} found",
                        f"{len(resume_info['certifications'])} found",
                        f"{resume_info['word_count']} words",
                        '✓ Present' if resume_info['email'] else '✗ Missing',
                        '✓ Present' if resume_info['phone'] else '✗ Missing',
                    ],
                    'Quality': [
                        '✓ Good' if len(resume_info['skills']) >= 8 else '⚠️ Needs work',
                        '✓ Good' if len(resume_info['education']) > 0 else '⚠️ Missing',
                        '✓ Good' if len(resume_info['certifications']) > 0 else '⚠️ Optional',
                        '✓ Good' if resume_info['word_count'] >= 500 else '⚠️ Too short',
                        '✓ Yes' if resume_info['email'] else '❌ No',
                        '✓ Yes' if resume_info['phone'] else '❌ No',
                    ],
                }
                st.table(pd.DataFrame(breakdown_data).astype(str))

                st.markdown("---")
                st.markdown("### 🎯 Pro Tips to Improve Your Score")
                tips_col1, tips_col2 = st.columns(2)
                with tips_col1:
                    st.info("**✓ Keyword Optimization**\n- Mirror keywords from job description\n- Use industry-specific terminology\n- Include both technical and soft skills")
                    st.info("**✓ Contact & Formatting**\n- Always include email and phone\n- Use clear section headings\n- Consistent date formatting")
                with tips_col2:
                    st.info("**✓ Content Strategy**\n- Use quantifiable achievements\n- Include years of experience\n- Add relevant certifications")
                    st.info("**✓ Length & Detail**\n- Maintain 600-1000 word count\n- Include full company names\n- Describe significant projects")


main()
