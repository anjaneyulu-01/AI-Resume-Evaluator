# Quick Start Guide 🚀

## Get Started in 3 Steps!

### Step 1: Install Dependencies (First Time Only)
Open PowerShell and run:
```powershell
cd d:\PROJECTS\Resume-Ats-Tracker
pip install -r requirements.txt
```

### Step 2: Start the Application
```powershell
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501`

### Step 3: Test Your Resume
1. **Copy your resume** and paste it into the text area, OR
2. **Click "Upload File"** to upload a TXT or PDF file
3. **Click the "Analyze Resume" button**
4. **Review your ATS score and recommendations**

---

## Testing with Sample Resume

A sample resume is included (`sample_resume.txt`) that should score ~85-90/100.

Try this to see how it works:
1. Open `sample_resume.txt`
2. Copy all content
3. Paste into the app
4. Analyze and see what a good resume looks like!

---

## Common Commands

| Task | Command |
|------|---------|
| First time setup | `pip install -r requirements.txt` |
| Run app | `streamlit run app.py` |
| Different port | `streamlit run app.py --server.port 8502` |
| Update packages | `pip install -r requirements.txt --upgrade` |
| Stop app | `Ctrl + C` |

---

## What Each Model Does

| File | Purpose |
|------|---------|
| `ats_model.pkl` | Main model that scores your resume 0-100 |
| `skills_vectorizer.pkl` | Converts detected skills into numeric format |
| `cert_encoder.pkl` | Encodes certification information |
| `edu_encoder.pkl` | Encodes education level information |

---

## Features Overview

✅ **Beautiful UI** - Modern, professional interface
✅ **Smart Analysis** - Detects skills, education, certifications
✅ **Actionable Feedback** - Get specific recommendations
✅ **Fast Processing** - Instant results
✅ **Easy Input** - Paste text or upload files
✅ **Detailed Breakdown** - See exactly what impacts your score

---

## Troubleshooting

**Problem**: App won't start
- Solution: Ensure Python 3.8+ is installed: `python --version`

**Problem**: Module not found errors
- Solution: Install requirements: `pip install -r requirements.txt`

**Problem**: Port 8501 in use
- Solution: Use different port: `streamlit run app.py --server.port 8502`

**Problem**: Model files not found
- Solution: Ensure all `.pkl` files are in `d:\PROJECTS\Resume-Ats-Tracker`

---

## Tips for Best Results

1. **Use clear formatting** - Use proper punctuation and structure
2. **Include keywords** - Use industry-specific terms from job description
3. **Add metrics** - Use numbers (e.g., "improved performance by 45%")
4. **Be specific** - Replace "worked on" with specific accomplishments
5. **Update regularly** - Add new skills and achievements
6. **Tailor for roles** - Customize for each application

---

**Ready to optimize your resume? Run the app now!** 🎉
