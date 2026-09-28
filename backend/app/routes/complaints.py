from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.models.complaint import Complaint, ComplaintComment, ComplaintStatus, PriorityLevel
from app.schemas.complaint import (
    ComplaintCreate, ComplaintResponse, CommentCreate, ComplaintListResponse, ComplaintUpdate
)
from app.middleware.auth import get_current_user, require_role

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

    new_complaint = Complaint(
        student_id=current_user.id,
        title=complaint_data.title,
        description=complaint_data.description
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
