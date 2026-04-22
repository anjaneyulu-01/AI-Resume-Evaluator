---
title: Resume ATS Tracker
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: streamlit
app_file: app.py
pinned: false
---

# 📄 Resume ATS Score Checker

An AI-powered tool that scores your resume against Applicant Tracking Systems (ATS) and gives actionable recommendations.

## Features

- **ATS Score (0–100)** using a trained Gradient Boosting model (R² = 97.4%)
- **Skill detection** across 100+ technical and soft-skill keywords
- **Contact info validation** (email, phone)
- **Education & certification parsing**
- **Personalized recommendations** ranked by priority
- Supports plain text paste or `.txt` / `.pdf` file upload

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```
├── app.py                  # Entry point
├── model/
│   ├── ats_model.pkl       # Trained Gradient Boosting model
│   ├── scaler.pkl          # Feature scaler
│   └── model_metadata.json # Model info
├── utils/
│   └── logic.py            # Core logic (extraction, scoring, recommendations)
└── requirements.txt
```

## Hugging Face Spaces Deployment

1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Set **SDK** to `Streamlit`
3. Push this repository:
   ```bash
   git remote add space https://huggingface.co/spaces/<your-username>/<space-name>
   git push space main
   ```
4. The Space will install `requirements.txt` and run `app.py` automatically.
