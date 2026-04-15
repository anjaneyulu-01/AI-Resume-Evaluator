# utils.py - Utility functions for resume analysis

import re
from config import SKILLS_TO_DETECT, EDUCATION_KEYWORDS, CERTIFICATION_KEYWORDS

def extract_contact_info(text):
    """Extract email and phone from text"""
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    phone_pattern = r'\b(\d{3}[-.]?\d{3}[-.]?\d{4})\b'
    
    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)
    
    return {
        'email': email.group(0) if email else None,
        'phone': phone.group(0) if phone else None,
    }

def extract_skills(text):
    """Extract technical skills from text"""
    text_lower = text.lower()
    found_skills = []
    
    for skill in SKILLS_TO_DETECT:
        if skill in text_lower:
            found_skills.append(skill)
    
    return list(set(found_skills))  # Remove duplicates

def extract_education(text):
    """Extract education information from text"""
    text_lower = text.lower()
    found_education = []
    
    for edu in EDUCATION_KEYWORDS:
        if edu in text_lower:
            found_education.append(edu)
    
    return list(set(found_education))

def extract_certifications(text):
    """Extract certifications from text"""
    text_lower = text.lower()
    found_certs = []
    
    for cert in CERTIFICATION_KEYWORDS:
        if cert in text_lower:
            found_certs.append(cert)
    
    return list(set(found_certs))

def validate_resume_text(text):
    """Validate if text is a valid resume"""
    if not text or not text.strip():
        return False, "Resume text is empty"
    
    if len(text) < 100:
        return False, "Resume is too short. Minimum 100 characters required."
    
    return True, "Resume is valid"

def get_resume_length_category(word_count):
    """Categorize resume length"""
    if word_count < 300:
        return "Too Short"
    elif word_count < 500:
        return "Short"
    elif word_count < 1000:
        return "Good"
    elif word_count < 1500:
        return "Lengthy"
    else:
        return "Too Long"
