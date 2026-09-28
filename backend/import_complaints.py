import csv
import sys
from pathlib import Path
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.complaint import Complaint, ComplaintCategory, PriorityLevel, ComplaintStatus
from app.models.user import User

CATEGORY_MAPPING = {
    "Fee/Payment": ComplaintCategory.FEE_PAYMENT,
    "Attendance": ComplaintCategory.ATTENDANCE,
    "Academic": ComplaintCategory.ACADEMIC,
    "Technical/IT": ComplaintCategory.TECHNICAL_IT,
    "Hostel": ComplaintCategory.HOSTEL,
    "Infrastructure/Maintenance": ComplaintCategory.INFRASTRUCTURE,
    "Examination": ComplaintCategory.EXAMINATION,
    "Scholarship/Financial Aid": ComplaintCategory.SCHOLARSHIP,
    "Library": ComplaintCategory.LIBRARY,
    "Transport": ComplaintCategory.TRANSPORT,
    "Student Welfare": ComplaintCategory.STUDENT_WELFARE,
}

PRIORITY_MAPPING = {
    "Low": PriorityLevel.LOW,
    "Medium": PriorityLevel.MEDIUM,
    "High": PriorityLevel.HIGH,
    "Critical": PriorityLevel.CRITICAL,
}

def get_or_create_student(db: Session):
    """Get existing student or create one for testing."""
    student = db.query(User).filter(User.email == "student@example.com").first()
    if not student:
        from app.utils.security import hash_password
        student = User(
            email="student@example.com",
            full_name="Student User",
            hashed_password=hash_password("student123"),
            role="student"
        )
        db.add(student)
        db.commit()
        db.refresh(student)
    return student

def import_complaints_from_csv(csv_path: str):
    """Import complaints from CSV file."""
    db = SessionLocal()

    try:
        # Get or create student
        student = get_or_create_student(db)
        print(f"✓ Using student: {student.email} (ID: {student.id})")

        # Read CSV and import
        complaints_list = []
        skipped = 0

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    category_str = row.get('category', '').strip()
                    priority_str = row.get('priority', 'Medium').strip()

                    # Map category
                    category = CATEGORY_MAPPING.get(category_str, ComplaintCategory.OTHER)

                    # Map priority
                    priority = PRIORITY_MAPPING.get(priority_str, PriorityLevel.MEDIUM)

                    complaint = Complaint(
                        student_id=student.id,
                        title=row.get('complaint_text', '').strip()[:200],  # Use complaint_text as title
                        description=row.get('complaint_text', '').strip(),
                        category=category,
                        assigned_department=row.get('department', '').strip(),
                        priority=priority,
                        status=ComplaintStatus.SUBMITTED
                    )
                    complaints_list.append(complaint)

                except Exception as e:
                    print(f"  ⚠ Skipped row {row.get('complaint_id', 'unknown')}: {str(e)}")
                    skipped += 1

        # Bulk insert
        if complaints_list:
            db.bulk_save_objects(complaints_list)
            db.commit()
            print(f"\n✓ Successfully imported {len(complaints_list)} complaints")

        if skipped > 0:
            print(f"⚠ Skipped {skipped} rows due to errors")

        # Print summary
        total = db.query(Complaint).count()
        print(f"\n📊 Database Summary:")
        print(f"  Total complaints: {total}")

        # Category breakdown
        print(f"\n  By Category:")
        category_counts = {}
        for complaint in db.query(Complaint).all():
            if complaint.category:
                cat_val = complaint.category.value
                category_counts[cat_val] = category_counts.get(cat_val, 0) + 1

        for cat, count in sorted(category_counts.items()):
            print(f"    {cat}: {count}")

        # Priority breakdown
        print(f"\n  By Priority:")
        for priority in [PriorityLevel.CRITICAL, PriorityLevel.HIGH, PriorityLevel.MEDIUM, PriorityLevel.LOW]:
            count = db.query(Complaint).filter(Complaint.priority == priority).count()
            if count > 0:
                print(f"    {priority.value}: {count}")

        print(f"\n✅ Import completed successfully!")

    except FileNotFoundError:
        print(f"❌ Error: File not found: {csv_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during import: {str(e)}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    csv_file = Path(__file__).parent / "complaints.csv"

    if not csv_file.exists():
        print(f"❌ complaints.csv not found at {csv_file}")
        sys.exit(1)

    print(f"📂 Importing from: {csv_file}\n")
    import_complaints_from_csv(str(csv_file))
