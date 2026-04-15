# Developer Guide

## Project Architecture

### Overview
Resume ATS Score Checker is a machine learning-powered web application that analyzes resumes and provides optimization recommendations.

### Tech Stack
- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python with scikit-learn
- **ML Models**: Pre-trained pickle files
- **Deployment**: Docker ready

### Project Structure

```
Resume-Ats-Tracker/
├── app.py                    # Main Streamlit application (USE THIS TO RUN)
├── config.py                 # Configuration and customization settings
├── utils.py                  # Utility functions for resume analysis
├── test_models.py           # Testing and validation script
│
├── ats_model.pkl            # Trained ATS scoring model
├── cert_encoder.pkl         # Certification encoder
├── edu_encoder.pkl          # Education level encoder
├── skills_vectorizer.pkl    # Skills vectorizer
│
├── sample_resume.txt        # Sample resume for testing
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
│
├── run.bat                 # Windows batch script (quick start)
├── run.ps1                 # PowerShell script (quick start)
│
├── README.md               # Main documentation
├── QUICKSTART.md           # Quick start guide (START HERE)
└── DEVELOPER_GUIDE.md      # This file
```

## Running the Application

### Option 1: Direct Python (Recommended for Development)
```bash
streamlit run app.py
```

### Option 2: Windows Batch Script
```bash
run.bat
```

### Option 3: PowerShell Script
```powershell
powershell -ExecutionPolicy Bypass -File run.ps1
```

### Option 4: Docker
```bash
docker-compose up --build
```

## Code Structure

### app.py - Main Application
The main Streamlit application with:
- Page configuration and styling
- Model loading
- Resume information extraction
- ATS score calculation
- UI rendering

**Key Components:**
- `load_models()` - Loads pickled ML models
- `extract_resume_info()` - Extracts skills, education, certifications
- `calculate_ats_score()` - Computes the ATS score
- `get_recommendations()` - Generates improvement suggestions
- `main()` - Renders the web interface

### config.py - Configuration
Centralized configuration for:
- Skills to detect (150+ technical skills)
- Education keywords
- Certification keywords
- Scoring weights
- UI theme colors
- Default recommendations

**Customization:**
Edit `config.py` to:
- Add new skills to detect
- Change scoring weights
- Modify threshold values
- Update recommendation messages

### utils.py - Utility Functions
Helper functions for:
- Contact information extraction
- Skill detection
- Education extraction
- Certification detection
- Resume validation
- Resume length categorization

**Available Functions:**
- `extract_contact_info(text)` - Returns email and phone
- `extract_skills(text)` - Returns list of detected skills
- `extract_education(text)` - Returns list of detected education
- `extract_certifications(text)` - Returns list of detected certifications
- `validate_resume_text(text)` - Validates resume content
- `get_resume_length_category(word_count)` - Categorizes resume length

## Extending the Application

### Adding New Skills Detection

1. Open `config.py`
2. Add new skills to the `SKILLS_TO_DETECT` list:
```python
SKILLS_TO_DETECT = [
    # ... existing skills
    'new_skill', 'another_skill',  # Add here
]
```

### Modifying Score Calculation

The scoring formula in `app.py`:
```python
score = min(max(score, 0), 100)  # Clamp between 0-100
```

To customize weights, modify the fallback calculation section or update the model weights in `config.py`.

### Adding New Features

To add new resume analysis features:

1. Create extraction function in `utils.py`:
```python
def extract_new_feature(text):
    # Your extraction logic
    return feature_data
```

2. Call it in `app.py`:
```python
resume_info = extract_resume_info(resume_text)
new_feature = extract_new_feature(resume_text)
```

3. Display results in the UI:
```python
st.metric("New Feature", new_feature)
```

### Improving the Model

To retrain the ATS model:

1. Prepare training data (resumes with labeled scores)
2. Extract features using `utils.py` functions
3. Train with scikit-learn:
```python
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(X_train, y_train)
pickle.dump(model, open('ats_model.pkl', 'wb'))
```

## Customization Guide

### Change Skill Detection

Edit `config.py` SKILLS_TO_DETECT to add domain-specific skills:
```python
SKILLS_TO_DETECT = [
    # Add industry-specific skills
    'specific_tool', 'specialized_language',
]
```

### Adjust Scoring Weights

In `config.py`, modify SCORE_WEIGHTS:
```python
SCORE_WEIGHTS = {
    'skill_count': 3,        # Increase importance of skills
    'education_count': 2,    # Decrease importance of education
}
```

### Change Color Theme

In `config.py` THEME_COLORS:
```python
THEME_COLORS = {
    'primary': '#YOUR_COLOR',
    'success': '#YOUR_COLOR',
}
```

And update CSS in `app.py` if needed.

## Testing

### Run Tests
```bash
python test_models.py
```

This will:
1. Load all trained models
2. Analyze the sample resume
3. Calculate ATS score
4. Display detailed breakdown
5. Verify all components work

### Manual Testing
1. Run the app: `streamlit run app.py`
2. Use sample resume provided
3. Check if score is as expected (~85-90)
4. Try your own resume and verify recommendations

## Deployment

### Local Network Access
To access from other computers on your network:
```bash
streamlit run app.py --server.address 0.0.0.0
```

Then access via: `http://YOUR_IP:8501`

### Docker Deployment
```bash
docker-compose up -d
```

Access at: `http://localhost:8501`

### Cloud Deployment (Streamlit Cloud)
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub account
4. Deploy directly from your repository

## Performance Optimization

### Model Loading
Models are cached using `@st.cache_resource` to avoid reloading:
```python
@st.cache_resource
def load_models():
    # Models loaded once per session
```

### Skip Inefficient Tasks
For faster processing:
- Comment out PDF support if not needed
- Reduce skill detection list if too many false positives
- Cache results by resume hash

## Troubleshooting

### Models Not Loading
- Ensure all `.pkl` files are in the same directory as `app.py`
- Check file permissions
- Verify pickle files aren't corrupted

### Low Scores on Good Resumes
- Check skill detection in `utils.py`
- Verify model predictions are reasonable
- Consider retraining the model

### PDF Upload Issues
- Install PyPDF2: `pip install PyPDF2`
- Test with PDF created using standard tools
- Check for OCR PDFs (text may not extract properly)

## Future Enhancements

### Planned Features
- [ ] Job description matching
- [ ] ATS keyword suggestions from JD
- [ ] Multi-language support
- [ ] Resume formatting analysis
- [ ] Batch processing
- [ ] Export reports as PDF
- [ ] Advanced NLP for better entity extraction
- [ ] Integration with job boards

### Potential Improvements
- Better education/certification recognition (using NER)
- More sophisticated keyword extraction
- Resume template detection and recommendations
- Competitive scoring against similar resumes

## References

### Libraries
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [NumPy Documentation](https://numpy.org/)

### ML Concepts
- Feature engineering for resume analysis
- Classification vs Regression for ATS scoring
- Model evaluation metrics

## Support

For issues or questions:
1. Check the README.md
2. Review QUICKSTART.md
3. Run `test_models.py` to verify setup
4. Check that all `.pkl` files are present
5. Ensure Python version is 3.8+

---

**Happy Developing! 🚀**
