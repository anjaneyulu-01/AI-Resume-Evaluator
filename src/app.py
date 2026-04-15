import streamlit as st
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import re
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Resume ATS Score Checker",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced custom CSS styling
st.markdown("""
    <style>
    /* Global Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        padding: 0rem;
    }
    
    /* Main Container */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
        font-weight: 800;
    }
    
    .main-header p {
        font-size: 1.1em;
        opacity: 0.95;
    }
    
    /* Score Display */
    .score-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 30px 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    .score-label {
        font-size: 16px;
        font-weight: 600;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .score-number {
        font-size: 72px;
        font-weight: 900;
        margin: 15px 0;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .score-rating {
        font-size: 24px;
        font-weight: 700;
        margin-top: 10px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 5px 15px rgba(245, 87, 108, 0.3);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 800;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.9;
    }
    
    /* Progress Bars */
    .progress-container {
        background: #e9ecef;
        height: 10px;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        transition: width 0.4s ease;
    }
    
    /* Skills Container */
    .skill-tag {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        margin: 5px 5px 5px 0;
    }
    
    .skill-tag-alt {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        margin: 5px 5px 5px 0;
    }
    
    /* Recommendation Item */
    .recommendation-item {
        background: white;
        border-left: 4px solid #667eea;
        padding: 20px;
        margin: 15px 0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .recommendation-priority {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 22px;
        font-weight: 700;
        margin: 30px 0 20px 0;
        padding-bottom: 12px;
        border-bottom: 3px solid #667eea;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# Load models with better error handling
@st.cache_resource
def load_models():
    try:
        models_dir = Path(__file__).parent.parent / 'models'
        
        # Try to load the new trained model
        try:
            with open(models_dir / 'ats_model.pkl', 'rb') as f:
                ats_model = pickle.load(f)
        except:
            ats_model = None
        
        # Try to load the scaler
        try:
            with open(models_dir / 'scaler.pkl', 'rb') as f:
                scaler = pickle.load(f)
        except:
            scaler = None
        
        # Try to load metadata
        try:
            with open(models_dir / 'model_metadata.json', 'r') as f:
                metadata = json.load(f)
        except:
            metadata = {'model_type': 'Fallback', 'test_r2_score': 0}
        
        return ats_model, scaler, metadata
    except:
        return None, None, {'model_type': 'Fallback'}

# Extract resume information
def extract_resume_info(resume_text):
    text_lower = resume_text.lower()
    
    skills_list = [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
        'kotlin', 'swift', 'matlab', 'scala',
        'sql', 'html', 'css', 'react', 'angular', 'vue', 'svelte',
        'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'asp.net',
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ci/cd',
        'git', 'github', 'gitlab', 'linux', 'windows', 'macos', 'unix',
        'machine learning', 'deep learning', 'nlp', 'computer vision', 'data analysis',
        'excel', 'powerpoint', 'tableau', 'power bi', 'looker', 'data visualization',
        'agile', 'scrum', 'jira', 'confluence', 'api', 'rest', 'graphql', 'websockets',
        'mongodb', 'postgresql', 'mysql', 'oracle', 'redis', 'elasticsearch', 'cassandra',
        'microservices', 'serverless', 'lambda', 'terraform', 'ansible',
        'leadership', 'communication', 'teamwork', 'problem solving', 'project management'
    ]
    
    education_keywords = ['bachelor', 'master', 'phd', 'doctorate', 'diploma', 'associate',
                         'engineering', 'science', 'technology', 'computer science']
    
    certification_keywords = ['aws certified', 'azure certified', 'kubernetes', 'scrum master',
                             'certified', 'pmp', 'cissp', 'gcp', 'google cloud']
    
    def _has_term(text: str, term: str) -> bool:
        # Strict boundary-based matching prevents false positives like "go" in "goal".
        pattern = r'(?<!\w)' + re.escape(term) + r'(?!\w)'
        return re.search(pattern, text) is not None

    found_skills = []
    for skill in skills_list:
        if _has_term(text_lower, skill):
            found_skills.append(skill)
    
    found_education = sorted(list(set([edu for edu in education_keywords if _has_term(text_lower, edu)])))
    found_certs = sorted(list(set([cert for cert in certification_keywords if _has_term(text_lower, cert)])))
    
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text)
    phone = re.search(r'\b(\d{3}[-.]?\d{3}[-.]?\d{4})\b', resume_text)
    
    return {
        'skills': sorted(list(set(found_skills))),
        'education': found_education,
        'certifications': found_certs,
        'email': email.group(0) if email else None,
        'phone': phone.group(0) if phone else None,
        'word_count': len(resume_text.split()),
        'has_experience_section': bool(re.search(r'(?i)\b(experience|work history|employment)\b', resume_text)),
        'has_projects_section': bool(re.search(r'(?i)\b(projects?|portfolio)\b', resume_text))
    }

# Calculate ATS score
def calculate_ats_score(resume_info, model, scaler):
    skills = resume_info['skills']
    education = resume_info['education']
    certs = resume_info['certifications']
    word_count = resume_info['word_count']
    has_email = 1 if resume_info['email'] else 0
    has_phone = 1 if resume_info['phone'] else 0
    
    features = np.array([[
        len(skills),
        len(education),
        len(certs),
        word_count,
        has_email,
        has_phone
    ]])
    
    raw_model_score = None
    try:
        if model is not None and scaler is not None:
            features_scaled = scaler.transform(features)
            raw_model_score = float(model.predict(features_scaled)[0])
    except:
        pass
    
    # Fallback calculation
    score = 8
    score += min(len(skills) * 3, 38)
    score += min(len(education) * 8, 20)
    score += min(len(certs) * 2.5, 10)
    
    if word_count < 250:
        score -= 22
    elif word_count < 400:
        score -= 10
    elif word_count < 700:
        score += 8
    elif word_count <= 1400:
        score += 14
    else:
        score += 5
    
    if has_email:
        score += 8
    else:
        score -= 15

    if has_phone:
        score += 4
    else:
        score -= 6

    # Structural penalties keep low-quality resumes from scoring too high.
    if len(skills) < 4:
        score -= 15
    elif len(skills) < 8:
        score -= 6

    if len(education) == 0:
        score -= 8

    if not resume_info.get('has_experience_section', False):
        score -= 10

    # Penalize keyword stuffing (too many skills per 100 words).
    skill_density = (len(skills) / max(word_count, 1)) * 100
    if skill_density > 6.0:
        score -= 8

    fallback_score = float(min(max(score, 0), 100))

    # Blend model + calibrated rules for robustness.
    if raw_model_score is not None:
        blended = (0.65 * raw_model_score) + (0.35 * fallback_score)
    else:
        blended = fallback_score

    # Guardrail: avoid unrealistic 99+ unless profile is truly complete.
    top_profile = (
        len(skills) >= 12 and
        len(education) >= 1 and
        has_email == 1 and
        has_phone == 1 and
        resume_info.get('has_experience_section', False) and
        500 <= word_count <= 1400
    )

    if not top_profile:
        blended = min(blended, 92.0)
    else:
        blended = min(blended, 98.0)
    
    return float(min(max(blended, 0), 100))

# Get personalized recommendations
def get_recommendations(resume_info, score):
    recs = []
    
    if resume_info['word_count'] < 300:
        recs.append({
            'priority': 'HIGH',
            'emoji': '📝',
            'title': 'Expand Resume Length',
            'detail': f'Your resume is too short ({resume_info["word_count"]} words). Aim for 600-1000 words with detailed achievements and responsibilities.'
        })
    
    if not resume_info['email']:
        recs.append({
            'priority': 'CRITICAL',
            'emoji': '📧',
            'title': 'Add Email Address',
            'detail': 'Include your professional email address at the top of your resume. Make it easy for recruiters to contact you.'
        })
    
    if not resume_info['phone']:
        recs.append({
            'priority': 'HIGH',
            'emoji': '☎️',
            'title': 'Include Phone Number',
            'detail': 'Add your phone number for direct contact opportunities. Format: (123) 456-7890'
        })
    
    if len(resume_info['skills']) < 5:
        recs.append({
            'priority': 'HIGH',
            'emoji': '🛠️',
            'title': 'Add More Technical Skills',
            'detail': f'You have only {len(resume_info["skills"])} skills. Include at least 8-12 relevant technical skills for your target role.'
        })
    
    if len(resume_info['skills']) < 3:
        recs.append({
            'priority': 'CRITICAL',
            'emoji': '⚠️',
            'title': 'Critical Skill Gap',
            'detail': 'Your resume lacks specific technical skills. Add programming languages, tools, and frameworks relevant to the position.'
        })
    
    if len(resume_info['education']) == 0:
        recs.append({
            'priority': 'MEDIUM',
            'emoji': '🎓',
            'title': 'Add Educational Background',
            'detail': 'Include your degrees, institution names, and graduation dates. This is important for many positions.'
        })
    
    if len(resume_info['certifications']) == 0:
        recs.append({
            'priority': 'LOW',
            'emoji': '🏆',
            'title': 'Highlight Certifications',
            'detail': 'Add any professional certifications or credentials you have. These boost your credibility.'
        })
    
    if score < 40:
        recs.append({
            'priority': 'CRITICAL',
            'emoji': '🚨',
            'title': 'Major Restructuring Needed',
            'detail': 'Your resume needs significant improvements. Focus on: contact info, skills, work experience details, and quantifiable achievements.'
        })
    elif score < 60:
        recs.append({
            'priority': 'HIGH',
            'emoji': '⚡',
            'title': 'Significant Improvements Needed',
            'detail': 'Implement the recommendations above to substantially improve your ATS score.'
        })
    
    return recs

def get_score_category(score):
    if score >= 85:
        return "🌟 Excellent", "#28a745"
    elif score >= 70:
        return "👍 Good", "#007bff"
    elif score >= 50:
        return "⚠️ Average", "#ffc107"
    else:
        return "❌ Needs Improvement", "#dc3545"

# Main app
def main():
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>📄 Resume ATS Score Checker</h1>
            <p>AI-powered optimization for Applicant Tracking Systems</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load models
    model, scaler, metadata = load_models()
    
    # Sidebar
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
        st.caption("""
        99% of Fortune 500 companies use ATS. Higher score = better chance of being reviewed!
        """)
    
    # Main content
    st.markdown("### 📥 Upload Your Resume")
    input_method = st.radio("Choose input method:", ["Paste Text", "Upload File"], horizontal=True)
    
    resume_text = ""
    
    if input_method == "Paste Text":
        resume_text = st.text_area(
            "Paste your resume text:",
            height=400,
            placeholder="Paste your complete resume here...",
            label_visibility="collapsed"
        )
    else:
        uploaded_file = st.file_uploader("Upload resume file:", type=["txt", "pdf"])
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                resume_text = uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "application/pdf":
                try:
                    import PyPDF2
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    resume_text = ""
                    for page in pdf_reader.pages:
                        resume_text += page.extract_text()
                except:
                    st.error("PDF parsing error. Try pasting text instead.")
    
    # Analyze button
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        analyze_button = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)
    
    # Analysis
    if analyze_button:
        if not resume_text.strip():
            st.error("❌ Please provide resume text to analyze.")
        else:
            with st.spinner("🔍 Analyzing your resume..."):
                # Extract info
                resume_info = extract_resume_info(resume_text)
                
                # Calculate score
                score = calculate_ats_score(resume_info, model, scaler)
                
                # Get category
                category, color = get_score_category(score)
                
                # Display score prominently
                st.markdown(f"""
                    <div class="score-container">
                        <div class="score-label">Your ATS Score</div>
                        <div class="score-number">{score:.1f}</div>
                        <div class="score-rating">{category}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Progress bar
                st.markdown(f"""
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {score}%"></div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Metrics
                st.markdown("### 📊 Resume Metrics")
                
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">🛠️ Skills</div>
                            <div class="metric-value">{len(resume_info['skills'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with metric_col2:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">🎓 Education</div>
                            <div class="metric-value">{len(resume_info['education'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with metric_col3:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">🏆 Certs</div>
                            <div class="metric-value">{len(resume_info['certifications'])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with metric_col4:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">📝 Words</div>
                            <div class="metric-value">{resume_info['word_count']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Detected content
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
                        skill_display = ""
                        for skill in resume_info['skills'][:12]:
                            skill_display += f'<span class="skill-tag">{skill}</span>'
                        st.markdown(skill_display, unsafe_allow_html=True)
                        if len(resume_info['skills']) > 12:
                            st.caption(f"... and {len(resume_info['skills']) - 12} more")
                    else:
                        st.warning("No skills detected. Add technical keywords!")
                
                # Education & Certifications
                st.markdown("---")
                
                exp_col1, exp_col2 = st.columns(2)
                
                with exp_col1:
                    st.markdown("#### 🎓 Education")
                    if resume_info['education']:
                        edu_display = ""
                        for edu in resume_info['education']:
                            edu_display += f'<span class="skill-tag-alt">{edu}</span>'
                        st.markdown(edu_display, unsafe_allow_html=True)
                    else:
                        st.info("Add your educational background for better scoring")
                
                with exp_col2:
                    st.markdown("#### 🏆 Certifications")
                    if resume_info['certifications']:
                        cert_display = ""
                        for cert in resume_info['certifications']:
                            cert_display += f'<span class="skill-tag-alt">{cert}</span>'
                        st.markdown(cert_display, unsafe_allow_html=True)
                    else:
                        st.info("Professional certifications boost your score")
                
                # Recommendations
                st.markdown("---")
                st.markdown("### 💡 Personalized Recommendations")
                
                recs = get_recommendations(resume_info, score)
                
                if recs:
                    for rec in recs:
                        priority_color = {
                            'CRITICAL': '#dc3545',
                            'HIGH': '#fd7e14',
                            'MEDIUM': '#ffc107',
                            'LOW': '#17a2b8'
                        }.get(rec['priority'], '#6c757d')
                        
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
                
                # Detailed breakdown
                st.markdown("---")
                st.markdown("### 📈 Detailed Breakdown")
                
                breakdown_data = {
                    'Component': [
                        'Skills Count',
                        'Education',
                        'Certifications',
                        'Word Count',
                        'Email',
                        'Phone'
                    ],
                    'Status': [
                        f"{len(resume_info['skills'])} detected",
                        f"{len(resume_info['education'])} found",
                        f"{len(resume_info['certifications'])} found",
                        f"{resume_info['word_count']} words",
                        '✓ Present' if resume_info['email'] else '✗ Missing',
                        '✓ Present' if resume_info['phone'] else '✗ Missing'
                    ],
                    'Quality': [
                        '✓ Good' if len(resume_info['skills']) >= 8 else '⚠️ Needs work',
                        '✓ Good' if len(resume_info['education']) > 0 else '⚠️ Missing',
                        '✓ Good' if len(resume_info['certifications']) > 0 else '⚠️ Optional',
                        '✓ Good' if resume_info['word_count'] >= 500 else '⚠️ Too short',
                        '✓ Yes' if resume_info['email'] else '❌ No',
                        '✓ Yes' if resume_info['phone'] else '❌ No'
                    ]
                }
                
                # Use a static table so the layout stays stable and does not shift.
                df = pd.DataFrame(breakdown_data).astype(str)
                st.table(df)
                
                # Tips
                st.markdown("---")
                st.markdown("### 🎯 Pro Tips to Improve Your Score")
                
                tips_col1, tips_col2 = st.columns(2)
                
                with tips_col1:
                    st.info("""
                    **✓ Keyword Optimization**
                    - Mirror keywords from job description
                    - Use industry-specific terminology
                    - Include both technical and soft skills
                    """)
                    
                    st.info("""
                    **✓ Contact & Formatting**
                    - Always include email and phone
                    - Use clear section headings
                    - Consistent date formatting
                    """)
                
                with tips_col2:
                    st.info("""
                    **✓ Content Strategy**
                    - Use quantifiable achievements
                    - Include years of experience
                    - Add relevant certifications
                    """)
                    
                    st.info("""
                    **✓ Length & Detail**
                    - Maintain 600-1000 word count
                    - Include full company names
                    - Describe significant projects
                    """)

if __name__ == "__main__":
    main()
