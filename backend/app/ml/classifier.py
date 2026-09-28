import pickle
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from typing import Tuple, Dict, List
import joblib

MODEL_DIR = Path(__file__).parent.parent.parent / "models"
MODEL_DIR.mkdir(exist_ok=True)

CATEGORY_MAP = {
    "Academic": "Academic",
    "Attendance": "Attendance",
    "Examination": "Examination",
    "Fee/Payment": "Fee/Payment",
    "Hostel": "Hostel",
    "Infrastructure/Maintenance": "Infrastructure/Maintenance",
    "Library": "Library",
    "Scholarship/Financial Aid": "Scholarship",
    "Student Welfare": "Student Welfare",
    "Technical/IT": "Technical/IT",
    "Transport": "Transport",
}

DEPARTMENT_MAP = {
    "Academic": "Academic",
    "Attendance": "Academic",
    "Examination": "Examination Cell",
    "Fee/Payment": "Accounts",
    "Hostel": "Hostel",
    "Infrastructure/Maintenance": "Maintenance",
    "Library": "Library",
    "Scholarship": "Student Welfare",
    "Student Welfare": "Student Welfare",
    "Technical/IT": "IT Support",
    "Transport": "Transport",
}

class ComplaintClassifier:
    def __init__(self):
        self.category_model_path = MODEL_DIR / "category_classifier.pkl"
        self.vectorizer_path = MODEL_DIR / "tfidf_vectorizer.pkl"
        self.label_encoder_path = MODEL_DIR / "label_encoder.pkl"

        self.vectorizer = None
        self.category_model = None
        self.label_encoder = None
        self.is_trained = False

        self._load_model()

    def _load_model(self):
        """Load trained model from disk if it exists."""
        if (self.category_model_path.exists() and
            self.vectorizer_path.exists() and
            self.label_encoder_path.exists()):
            try:
                self.vectorizer = joblib.load(self.vectorizer_path)
                self.category_model = joblib.load(self.category_model_path)
                self.label_encoder = joblib.load(self.label_encoder_path)
                self.is_trained = True
            except Exception as e:
                print(f"⚠ Error loading model: {e}. Will train new model.")

    def train(self, texts: List[str], categories: List[str]):
        """Train the ML classifier on provided data."""
        print("🤖 Training ML classifier...")

        # Encode categories
        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(categories)

        # Vectorize text
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            min_df=2,
            max_df=0.8,
            ngram_range=(1, 2),
            lowercase=True,
            stop_words='english'
        )
        X = self.vectorizer.fit_transform(texts)

        # Train classifier
        self.category_model = MultinomialNB(alpha=0.1)
        self.category_model.fit(X, y)

        self.is_trained = True
        self._save_model()
        print(f"✅ Model trained on {len(texts)} samples")

    def _save_model(self):
        """Save trained model to disk."""
        joblib.dump(self.vectorizer, self.vectorizer_path)
        joblib.dump(self.category_model, self.category_model_path)
        joblib.dump(self.label_encoder, self.label_encoder_path)

    def predict(self, text: str) -> Dict[str, any]:
        """Predict category and confidence for a complaint."""
        if not self.is_trained:
            return {
                "category": "Other",
                "department": "Student Welfare",
                "confidence": 0.0,
                "error": "Model not trained yet"
            }

        try:
            # Vectorize input
            X = self.vectorizer.transform([text])

            # Get probabilities
            probabilities = self.category_model.predict_proba(X)[0]
            predicted_idx = np.argmax(probabilities)
            confidence = float(probabilities[predicted_idx])

            # Get category name
            category = self.label_encoder.classes_[predicted_idx]

            # Map to output category format
            output_category = CATEGORY_MAP.get(category, "Other")
            department = DEPARTMENT_MAP.get(output_category, "Student Welfare")

            return {
                "category": output_category,
                "department": department,
                "confidence": round(confidence, 3),
                "error": None
            }

        except Exception as e:
            return {
                "category": "Other",
                "department": "Student Welfare",
                "confidence": 0.0,
                "error": str(e)
            }

    def get_class_distribution(self) -> Dict[str, int]:
        """Get training distribution of categories."""
        if not self.is_trained or self.label_encoder is None:
            return {}

        return {
            cat: int(count)
            for cat, count in zip(
                self.label_encoder.classes_,
                np.bincount(self.label_encoder.transform(self.label_encoder.classes_))
            )
        }

# Global classifier instance
_classifier = None

def get_classifier() -> ComplaintClassifier:
    """Get or initialize the global classifier instance."""
    global _classifier
    if _classifier is None:
        _classifier = ComplaintClassifier()
    return _classifier
