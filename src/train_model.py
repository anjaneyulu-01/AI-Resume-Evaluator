# train_model.py - Create and train new ATS scoring model

import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pathlib import Path
import json

# Generate synthetic training data based on real resume characteristics
def create_training_data():
    """Create stricter and better-balanced synthetic training data for ATS scoring."""
    np.random.seed(42)
    
    n_samples = 4000
    
    # Features: [skills_count, education_count, cert_count, word_count, has_email, has_phone]
    X = []
    y = []
    
    for _ in range(n_samples):
        # Generate more realistic feature combinations with broad quality coverage.
        profile_type = np.random.choice(['weak', 'average', 'strong'], p=[0.35, 0.45, 0.20])

        if profile_type == 'weak':
            skills_count = np.random.randint(0, 7)
            education_count = np.random.randint(0, 2)
            cert_count = np.random.randint(0, 2)
            word_count = np.random.randint(120, 500)
        elif profile_type == 'average':
            skills_count = np.random.randint(5, 13)
            education_count = np.random.randint(1, 3)
            cert_count = np.random.randint(0, 4)
            word_count = np.random.randint(350, 1100)
        else:
            skills_count = np.random.randint(10, 21)
            education_count = np.random.randint(1, 4)
            cert_count = np.random.randint(1, 6)
            word_count = np.random.randint(600, 1700)

        has_email = np.random.randint(0, 2)  # 0 or 1
        has_phone = np.random.randint(0, 2)  # 0 or 1
        
        X.append([skills_count, education_count, cert_count, word_count, has_email, has_phone])
        
        # Create stricter target score so weak resumes stay low.
        score = 5

        # Skills contribution (diminishing returns)
        if skills_count < 3:
            score += skills_count * 2
        elif skills_count <= 12:
            score += 6 + (skills_count - 3) * 2.8
        else:
            score += 31.2 + min(skills_count - 12, 8) * 1.2

        # Education contribution
        if education_count == 0:
            score += 0
        elif education_count == 1:
            score += 8
        elif education_count == 2:
            score += 14
        else:
            score += 18

        # Certifications contribution
        score += min(cert_count * 2.0, 9)

        # Word count quality band
        if word_count < 220:
            score -= 20
        elif word_count < 350:
            score -= 10
        elif word_count < 600:
            score += 6
        elif word_count <= 1200:
            score += 14
        elif word_count <= 1800:
            score += 9
        else:
            score += 3

        # Contact details
        score += 8 if has_email else -14
        score += 4 if has_phone else -6

        # Add controlled noise
        score += np.random.normal(0, 4)
        
        # Ensure score is between 0-100
        score = min(max(score, 0), 100)
        
        y.append(score)
    
    return np.array(X), np.array(y)

def train_model():
    """Train the ATS scoring model"""
    print("🤖 Creating training data...")
    X, y = create_training_data()
    
    print(f"   Generated {len(X)} samples")
    print(f"   Feature shape: {X.shape}")
    print(f"   Score range: {y.min():.1f} - {y.max():.1f}")
    print(f"   Mean score : {y.mean():.1f}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    print("\n📊 Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model (good balance of accuracy and interpretability)
    print("🎯 Training Random Forest model...")
    rf_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train_scaled, y_train)
    
    # Train Gradient Boosting model (often more accurate)
    print("🎯 Training Gradient Boosting model...")
    gb_model = GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    gb_model.fit(X_train_scaled, y_train)
    
    # Evaluate models
    rf_score = rf_model.score(X_test_scaled, y_test)
    gb_score = gb_model.score(X_test_scaled, y_test)

    rf_pred = rf_model.predict(X_test_scaled)
    gb_pred = gb_model.predict(X_test_scaled)

    rf_mae = mean_absolute_error(y_test, rf_pred)
    gb_mae = mean_absolute_error(y_test, gb_pred)
    rf_rmse = float(np.sqrt(mean_squared_error(y_test, rf_pred)))
    gb_rmse = float(np.sqrt(mean_squared_error(y_test, gb_pred)))
    
    print(f"\n📈 Random Forest R² score: {rf_score:.4f}")
    print(f"📈 Gradient Boosting R² score: {gb_score:.4f}")
    print(f"📉 Random Forest MAE: {rf_mae:.2f}, RMSE: {rf_rmse:.2f}")
    print(f"📉 Gradient Boosting MAE: {gb_mae:.2f}, RMSE: {gb_rmse:.2f}")
    
    # Use the better model
    if gb_score > rf_score:
        print("\n✅ Using Gradient Boosting model (better performance)")
        final_model = gb_model
        model_name = "Gradient Boosting"
    else:
        print("\n✅ Using Random Forest model")
        final_model = rf_model
        model_name = "Random Forest"
    
    # Save models
    print("\n💾 Saving models...")
    models_dir = Path(__file__).parent.parent / 'models'
    
    with open(models_dir / 'ats_model.pkl', 'wb') as f:
        pickle.dump(final_model, f)
    
    with open(models_dir / 'scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    # Save metadata
    metadata = {
        'model_type': model_name,
        'features': ['skills_count', 'education_count', 'cert_count', 'word_count', 'has_email', 'has_phone'],
        'test_r2_score': float(max(rf_score, gb_score)),
        'test_mae': float(gb_mae if gb_score > rf_score else rf_mae),
        'test_rmse': float(gb_rmse if gb_score > rf_score else rf_rmse),
        'training_samples': len(X),
        'test_samples': len(X_test)
    }
    
    with open(models_dir / 'model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"   ✓ Model saved: ats_model.pkl")
    print(f"   ✓ Scaler saved: scaler.pkl")
    print(f"   ✓ Metadata saved: model_metadata.json")
    
    print("\n" + "="*60)
    print("✅ Model training completed successfully!")
    print("="*60)
    
    return final_model, scaler, metadata

if __name__ == "__main__":
    train_model()
