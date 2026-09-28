from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.models.complaint import Complaint, ComplaintComment, ComplaintStatus, PriorityLevel, ComplaintCategory
from app.schemas.complaint import (
    ComplaintCreate, ComplaintResponse, CommentCreate, ComplaintListResponse, ComplaintUpdate
)
from app.middleware.auth import get_current_user, require_role
from app.ml.classifier import get_classifier

router = APIRouter(prefix="/api/complaints", tags=["complaints"])

@router.post("/", response_model=ComplaintResponse)
def submit_complaint(
    complaint_data: ComplaintCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can submit complaints"
        )

    classifier = get_classifier()

    combined_text = f"{complaint_data.title}. {complaint_data.description}"
    prediction = classifier.predict(combined_text)

    category_value = prediction['category']
    try:
        category = ComplaintCategory(category_value)
    except ValueError:
        category = ComplaintCategory.OTHER

    new_complaint = Complaint(
        student_id=current_user.id,
        title=complaint_data.title,
        description=complaint_data.description,
        category=category,
        assigned_department=prediction['department'],
        confidence_score=prediction['confidence'],
        status=ComplaintStatus.SUBMITTED
    )
    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)
    return new_complaint

@router.get("/", response_model=List[ComplaintListResponse])
def get_complaints(
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status_filter: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Complaint)

    if current_user.role == UserRole.STUDENT:
        query = query.filter(Complaint.student_id == current_user.id)
    elif current_user.role == UserRole.DEPARTMENT_STAFF:
        query = query.filter(Complaint.assigned_department == current_user.department_id)

    if status_filter:
        try:
            status_enum = ComplaintStatus[status_filter.upper()]
            query = query.filter(Complaint.status == status_enum)
        except KeyError:
            pass

    complaints = query.offset(skip).limit(limit).all()
    return complaints

@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint_detail(
    complaint_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()

    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )

    if current_user.role == UserRole.STUDENT and complaint.student_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own complaints"
        )

    return complaint

@router.put("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(
    complaint_id: int,
    update_data: ComplaintUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()

    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )

    if current_user.role not in [UserRole.DEPARTMENT_STAFF, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff and admins can update complaints"
        )

    if update_data.status:
        complaint.status = update_data.status
    if update_data.resolution:
        complaint.resolution = update_data.resolution

    db.commit()
    db.refresh(complaint)
    return complaint

@router.post("/{complaint_id}/comments", response_model=dict)
def add_comment(
    complaint_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()

    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )

    new_comment = ComplaintComment(
        complaint_id=complaint_id,
        user_id=current_user.id,
        comment_text=comment_data.comment_text
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {"id": new_comment.id, "message": "Comment added successfully"}

@router.post("/ml/classify", response_model=dict)
def classify_text(
    text: dict,
    current_user: User = Depends(get_current_user)
):
    classifier = get_classifier()
    complaint_text = text.get("text", "")

    if not complaint_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text field is required"
        )

    prediction = classifier.predict(complaint_text)
    return {
        "text": complaint_text[:100] + "..." if len(complaint_text) > 100 else complaint_text,
        "predicted_category": prediction['category'],
        "assigned_department": prediction['department'],
        "confidence_score": prediction['confidence'],
        "model_status": "trained" if classifier.is_trained else "not_trained"
    }

@router.get("/ml/stats", response_model=dict)
def get_ml_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    classifier = get_classifier()

    total_complaints = db.query(Complaint).count()
    classified_complaints = db.query(Complaint).filter(Complaint.category != None).count()
    avg_confidence = db.query(Complaint).filter(
        Complaint.confidence_score != None
    ).all()

    avg_conf = 0.0
    if avg_confidence:
        avg_conf = sum(c.confidence_score for c in avg_confidence) / len(avg_confidence)

    category_stats = {}
    for complaint in db.query(Complaint).all():
        if complaint.category:
            cat = complaint.category.value
            category_stats[cat] = category_stats.get(cat, 0) + 1

    return {
        "model_trained": classifier.is_trained,
        "total_complaints": total_complaints,
        "auto_classified": classified_complaints,
        "classification_rate": round(classified_complaints / total_complaints * 100, 2) if total_complaints > 0 else 0,
        "average_confidence": round(avg_conf, 3),
        "category_distribution": category_stats
    }
