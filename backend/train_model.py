import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.complaint import Complaint
from app.ml.classifier import get_classifier

def train_ml_model():
    """Train the ML model on existing complaints."""
    db = SessionLocal()

    try:
        # Fetch all complaints with category
        complaints = db.query(Complaint).filter(
            Complaint.category != None,
            Complaint.description != None
        ).all()

        if not complaints:
            print("❌ No complaints found in database. Run import_complaints.py first.")
            sys.exit(1)

        print(f"\n📊 Found {len(complaints)} complaints for training")

        # Extract texts and categories
        texts = [c.description for c in complaints]
        categories = [c.category.value for c in complaints]

        # Get classifier and train
        classifier = get_classifier()
        classifier.train(texts, categories)

        # Print statistics
        print(f"\n✅ Model training complete!")
        print(f"\n📈 Category distribution:")
        category_dist = {}
        for cat in categories:
            category_dist[cat] = category_dist.get(cat, 0) + 1

        for cat, count in sorted(category_dist.items()):
            print(f"  {cat}: {count}")

        # Test on a sample
        print(f"\n🧪 Testing on sample complaints:")
        sample_count = min(3, len(complaints))
        for i in range(sample_count):
            complaint = complaints[i]
            prediction = classifier.predict(complaint.description)
            print(f"\n  Sample {i+1}:")
            print(f"    Actual: {complaint.category.value}")
            print(f"    Predicted: {prediction['category']} ({prediction['confidence']*100:.1f}%)")
            print(f"    Department: {prediction['department']}")

        print(f"\n✅ Model ready for inference!")

    except Exception as e:
        print(f"❌ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting ML model training...\n")
    train_ml_model()
