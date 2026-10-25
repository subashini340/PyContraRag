import xgboost as xgb
import numpy as np
import pandas as pd
import joblib
from src.config import MODELS_DIR

class CredibilityScorer:
    def __init__(self):
        self.model_path = MODELS_DIR / "credibility_model.pkl"
        self.model = None
        self._load_or_train()

    def _load_or_train(self):
        if self.model_path.exists():
            self.model = joblib.load(self.model_path)
            print("✅ Loaded existing credibility model.")
        else:
            print("⚙️ Training new credibility model...")
            self._train_model()

    def _train_model(self):
        # Dummy data to train the model (Features: [Version_Number, Is_Official_Docs])
        # Target: Credibility Score (0 to 1)
        X = np.array([
            [3.6, 1], [3.7, 1], [3.10, 1], [3.12, 1],  # Official Docs (High trust)
            [3.6, 0], [3.10, 0]                        # Unofficial blogs (Low trust)
        ])
        y = np.array([0.40, 0.60, 0.95, 0.99, 0.20, 0.50])
        
        # Train XGBoost Regressor
        self.model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=10)
        self.model.fit(X, y)
        
        # Save model for future use
        joblib.dump(self.model, self.model_path)
        print("✅ Credibility model trained and saved.")

    def get_score(self, version: float, is_official: int = 1) -> float:
        """Predicts credibility score based on version and source type."""
        if self.model is None:
            return 0.5
            
        features = np.array([[version, is_official]])
        score = self.model.predict(features)[0]
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, float(score)))

# --- Test block ---
if __name__ == "__main__":
    scorer = CredibilityScorer()
    
    # Testing with sample values
    score_36 = scorer.get_score(version=3.6, is_official=1)
    score_310 = scorer.get_score(version=3.10, is_official=1)
    
    print(f"\nPython 3.6 Docs Credibility:  {score_36:.2f}")
    print(f"Python 3.10 Docs Credibility: {score_310:.2f}")