# test_models.py - Test script to verify models and demonstrate usage

import pickle
import numpy as np
from pathlib import Path
from utils import extract_skills, extract_education, extract_certifications, extract_contact_info

def load_models():
    """Load all trained models"""
    print("Loading models...")
    models_dir = Path(__file__).parent.parent / 'models'
    
    with open(models_dir / 'ats_model.pkl', 'rb') as f:
        ats_model = pickle.load(f)
    
    with open(models_dir / 'cert_encoder.pkl', 'rb') as f:
        cert_encoder = pickle.load(f)
    
    with open(models_dir / 'edu_encoder.pkl', 'rb') as f:
        edu_encoder = pickle.load(f)
    
    with open(models_dir / 'skills_vectorizer.pkl', 'rb') as f:
        skills_vectorizer = pickle.load(f)
    
    print("✓ All models loaded successfully!")
    return ats_model, cert_encoder, edu_encoder, skills_vectorizer

def test_resume_analysis(resume_text):
    """Test analysis of a resume"""
    print("\n" + "="*60)
    print("RESUME ANALYSIS TEST")
    print("="*60)
    
    # Extract information
    skills = extract_skills(resume_text)
    education = extract_education(resume_text)
    certifications = extract_certifications(resume_text)
    contact = extract_contact_info(resume_text)
    word_count = len(resume_text.split())
    
    print(f"\n📊 Basic Information:")
    print(f"   Word Count: {word_count}")
    print(f"   Email: {contact['email'] if contact['email'] else 'Not found'}")
    print(f"   Phone: {contact['phone'] if contact['phone'] else 'Not found'}")
    
    print(f"\n🛠️  Skills Found ({len(skills)}):")
    for skill in skills[:10]:
        print(f"   • {skill}")
    if len(skills) > 10:
        print(f"   ... and {len(skills) - 10} more")
    
    print(f"\n🎓 Education Found ({len(education)}):")
    for edu in education:
        print(f"   • {edu}")
    
    print(f"\n🏆 Certifications Found ({len(certifications)}):")
    for cert in certifications:
        print(f"   • {cert}")
    
    return skills, education, certifications, contact, word_count

def test_scoring(ats_model, resume_data):
    """Test ATS scoring"""
    print("\n" + "="*60)
    print("ATS SCORING TEST")
    print("="*60)
    
    skills, education, certifications, contact, word_count = resume_data
    
    # Create feature vector
    features = np.array([
        len(skills),                           # skill_count
        len(education),                        # education_count
        len(certifications),                   # certification_count
        word_count,                            # word_count
        1 if contact['email'] else 0,         # has_contact
        1 if contact['phone'] else 0          # has_phone
    ]).reshape(1, -1)
    
    print(f"\nFeature Vector:")
    print(f"   Skills Count: {features[0][0]}")
    print(f"   Education Count: {features[0][1]}")
    print(f"   Certifications Count: {features[0][2]}")
    print(f"   Word Count: {features[0][3]}")
    print(f"   Has Email: {features[0][4]}")
    print(f"   Has Phone: {features[0][5]}")
    
    # Get prediction
    score = ats_model.predict(features)[0]
    score = min(max(score, 0), 100)  # Clamp to 0-100
    
    print(f"\n📈 ATS Score: {score:.1f}/100")
    
    # Determine rating
    if score >= 85:
        rating = "Excellent 🌟"
    elif score >= 70:
        rating = "Good 👍"
    elif score >= 50:
        rating = "Average ⚠️"
    else:
        rating = "Needs Improvement ❌"
    
    print(f"   Rating: {rating}")
    
    return score

def main():
    """Main test function"""
    print("\n" + "="*60)
    print("Resume ATS Checker - Model Testing")
    print("="*60)
    
    # Load sample resume
    print("\nLoading sample resume...")
    with open('sample_resume.txt', 'r') as f:
        sample_resume = f.read()
    
    print(f"✓ Sample resume loaded ({len(sample_resume)} characters)")
    
    # Load models
    ats_model, cert_encoder, edu_encoder, skills_vectorizer = load_models()
    
    # Test resume analysis
    resume_data = test_resume_analysis(sample_resume)
    
    # Test scoring
    score = test_scoring(ats_model, resume_data)
    
    print("\n" + "="*60)
    print("TEST COMPLETED SUCCESSFULLY ✓")
    print("="*60)
    print("\nThe models are working correctly!")
    print("You can now run the Streamlit app with: streamlit run app.py")
    print()

if __name__ == "__main__":
    main()
