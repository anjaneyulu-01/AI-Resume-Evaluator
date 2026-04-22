import re
import numpy as np

SKILLS_LIST = [
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
    'kotlin', 'swift', 'matlab', 'scala', 'perl', 'visual basic', 'r',
    'sql', 'html', 'css', 'react', 'angular', 'vue', 'svelte', 'next.js',
    'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'asp.net',
    'react native', 'flutter', 'ios', 'android',
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib',
    'machine learning', 'deep learning', 'nlp', 'computer vision', 'data analysis',
    'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
    'docker', 'kubernetes', 'jenkins', 'ci/cd', 'terraform', 'ansible',
    'git', 'github', 'gitlab', 'linux', 'windows', 'macos', 'unix', 'bash',
    'excel', 'powerpoint', 'tableau', 'power bi', 'looker', 'data visualization',
    'agile', 'scrum', 'jira', 'confluence', 'api', 'rest', 'graphql', 'websockets',
    'mongodb', 'postgresql', 'mysql', 'oracle', 'redis', 'elasticsearch', 'cassandra',
    'microservices', 'serverless', 'lambda',
    'leadership', 'communication', 'teamwork', 'problem solving', 'project management',
    'bootstrap', 'tailwind', 'webpack', 'sass', 'npm',
    'junit', 'pytest', 'selenium', 'cypress', 'jest', 'testing',
    'spark', 'hadoop', 'firebase', 'dynamodb', 'nosql',
]

EDUCATION_KEYWORDS = [
    'bachelor', 'bachelors', 'master', 'masters', 'mba', 'msc',
    'phd', 'doctorate', 'diploma', 'associate',
    'engineering', 'science', 'technology', 'computer science',
    'information technology', 'software engineering',
]

CERTIFICATION_KEYWORDS = [
    'aws certified', 'azure certified', 'kubernetes', 'scrum master',
    'certified', 'pmp', 'cissp', 'gcp', 'google cloud',
    'cka', 'ckad', 'comptia', 'network+', 'security+',
    'oracle certified', 'salesforce certified', 'microsoft certified',
]


def _match(text: str, term: str) -> bool:
    pattern = r'(?<!\w)' + re.escape(term) + r'(?!\w)'
    return re.search(pattern, text) is not None


def extract_resume_info(resume_text: str) -> dict:
    if not resume_text or not resume_text.strip():
        return {
            'skills': [], 'education': [], 'certifications': [],
            'email': None, 'phone': None, 'word_count': 0,
            'has_experience_section': False, 'has_projects_section': False,
        }

    text_lower = resume_text.lower()

    found_skills = sorted({s for s in SKILLS_LIST if _match(text_lower, s)})
    found_education = sorted({e for e in EDUCATION_KEYWORDS if _match(text_lower, e)})
    found_certs = sorted({c for c in CERTIFICATION_KEYWORDS if _match(text_lower, c)})

    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text)
    phone = re.search(r'\b(\d{3}[-.]?\d{3}[-.]?\d{4})\b', resume_text)

    return {
        'skills': found_skills,
        'education': found_education,
        'certifications': found_certs,
        'email': email.group(0) if email else None,
        'phone': phone.group(0) if phone else None,
        'word_count': len(resume_text.split()),
        'has_experience_section': bool(re.search(r'(?i)\b(experience|work history|employment)\b', resume_text)),
        'has_projects_section': bool(re.search(r'(?i)\b(projects?|portfolio)\b', resume_text)),
    }


def calculate_ats_score(resume_info: dict, model, scaler) -> float:
    skills = resume_info['skills']
    education = resume_info['education']
    certs = resume_info['certifications']
    word_count = resume_info['word_count']
    has_email = 1 if resume_info['email'] else 0
    has_phone = 1 if resume_info['phone'] else 0

    features = np.array([[len(skills), len(education), len(certs), word_count, has_email, has_phone]])

    raw_model_score = None
    try:
        if model is not None and scaler is not None:
            raw_model_score = float(model.predict(scaler.transform(features))[0])
    except Exception:
        pass

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

    score += 8 if has_email else -15
    score += 4 if has_phone else -6

    if len(skills) < 4:
        score -= 15
    elif len(skills) < 8:
        score -= 6

    if len(education) == 0:
        score -= 8

    if not resume_info.get('has_experience_section', False):
        score -= 10

    skill_density = (len(skills) / max(word_count, 1)) * 100
    if skill_density > 6.0:
        score -= 8

    fallback_score = float(min(max(score, 0), 100))

    blended = (0.65 * raw_model_score + 0.35 * fallback_score) if raw_model_score is not None else fallback_score

    top_profile = (
        len(skills) >= 12 and len(education) >= 1 and
        has_email == 1 and has_phone == 1 and
        resume_info.get('has_experience_section', False) and
        500 <= word_count <= 1400
    )
    blended = min(blended, 98.0 if top_profile else 92.0)

    return float(min(max(blended, 0), 100))


def get_recommendations(resume_info: dict, score: float) -> list:
    recs = []

    if resume_info['word_count'] < 300:
        recs.append({
            'priority': 'HIGH', 'emoji': '📝',
            'title': 'Expand Resume Length',
            'detail': f'Your resume is too short ({resume_info["word_count"]} words). Aim for 600-1000 words with detailed achievements and responsibilities.',
        })
    if not resume_info['email']:
        recs.append({
            'priority': 'CRITICAL', 'emoji': '📧',
            'title': 'Add Email Address',
            'detail': 'Include your professional email address at the top of your resume.',
        })
    if not resume_info['phone']:
        recs.append({
            'priority': 'HIGH', 'emoji': '☎️',
            'title': 'Include Phone Number',
            'detail': 'Add your phone number for direct contact opportunities. Format: (123) 456-7890',
        })
    if len(resume_info['skills']) < 5:
        recs.append({
            'priority': 'HIGH', 'emoji': '🛠️',
            'title': 'Add More Technical Skills',
            'detail': f'You have only {len(resume_info["skills"])} skills. Include at least 8-12 relevant technical skills for your target role.',
        })
    if len(resume_info['skills']) < 3:
        recs.append({
            'priority': 'CRITICAL', 'emoji': '⚠️',
            'title': 'Critical Skill Gap',
            'detail': 'Your resume lacks specific technical skills. Add programming languages, tools, and frameworks relevant to the position.',
        })
    if len(resume_info['education']) == 0:
        recs.append({
            'priority': 'MEDIUM', 'emoji': '🎓',
            'title': 'Add Educational Background',
            'detail': 'Include your degrees, institution names, and graduation dates.',
        })
    if len(resume_info['certifications']) == 0:
        recs.append({
            'priority': 'LOW', 'emoji': '🏆',
            'title': 'Highlight Certifications',
            'detail': 'Add any professional certifications or credentials you have.',
        })
    if score < 40:
        recs.append({
            'priority': 'CRITICAL', 'emoji': '🚨',
            'title': 'Major Restructuring Needed',
            'detail': 'Your resume needs significant improvements. Focus on: contact info, skills, work experience details, and quantifiable achievements.',
        })
    elif score < 60:
        recs.append({
            'priority': 'HIGH', 'emoji': '⚡',
            'title': 'Significant Improvements Needed',
            'detail': 'Implement the recommendations above to substantially improve your ATS score.',
        })

    return recs


def get_score_category(score: float) -> tuple:
    if score >= 85:
        return "🌟 Excellent", "#28a745"
    elif score >= 70:
        return "👍 Good", "#007bff"
    elif score >= 50:
        return "⚠️ Average", "#ffc107"
    else:
        return "❌ Needs Improvement", "#dc3545"
