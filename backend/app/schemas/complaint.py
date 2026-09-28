from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.complaint import ComplaintCategory, PriorityLevel, ComplaintStatus

class ComplaintCommentResponse(BaseModel):
    id: int
    user_id: int
    comment_text: str
    created_at: datetime

    class Config:
        from_attributes = True

class ComplaintBase(BaseModel):
    title: str
    description: str

class ComplaintCreate(ComplaintBase):
    pass

class ComplaintUpdate(BaseModel):
    status: Optional[ComplaintStatus] = None
    resolution: Optional[str] = None

class ComplaintResponse(ComplaintBase):
    id: int
    student_id: int
    category: Optional[ComplaintCategory]
    assigned_department: Optional[str]
    priority: PriorityLevel
    status: ComplaintStatus
    confidence_score: Optional[float]
    resolution: Optional[str]
    created_at: datetime
    updated_at: datetime
    comments: List[ComplaintCommentResponse] = []

    class Config:
        from_attributes = True

class ComplaintListResponse(BaseModel):
    id: int
    title: str
    category: Optional[ComplaintCategory]
    priority: PriorityLevel
    status: ComplaintStatus
    created_at: datetime

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    comment_text: str
