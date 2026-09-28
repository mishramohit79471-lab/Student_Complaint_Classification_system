from sqlalchemy import Column, Integer, String, Text, Enum, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class ComplaintCategory(str, enum.Enum):
    FEE_PAYMENT = "Fee/Payment"
    ATTENDANCE = "Attendance"
    ACADEMIC = "Academic"
    TECHNICAL_IT = "Technical/IT"
    HOSTEL = "Hostel"
    INFRASTRUCTURE = "Infrastructure/Maintenance"
    EXAMINATION = "Examination"
    SCHOLARSHIP = "Scholarship"
    LIBRARY = "Library"
    TRANSPORT = "Transport"
    STUDENT_WELFARE = "Student Welfare"
    OTHER = "Other"

class PriorityLevel(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class ComplaintStatus(str, enum.Enum):
    SUBMITTED = "Submitted"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(ComplaintCategory), nullable=True)
    assigned_department = Column(String, nullable=True)
    priority = Column(Enum(PriorityLevel), default=PriorityLevel.MEDIUM)
    status = Column(Enum(ComplaintStatus), default=ComplaintStatus.SUBMITTED)
    confidence_score = Column(Float, nullable=True)
    resolution = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

    student = relationship("User", foreign_keys=[student_id], back_populates="complaints")
    comments = relationship("ComplaintComment", back_populates="complaint", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Complaint(id={self.id}, category={self.category}, status={self.status})>"

class ComplaintComment(Base):
    __tablename__ = "complaint_comments"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    complaint = relationship("Complaint", back_populates="comments")
    user = relationship("User")

    def __repr__(self):
        return f"<ComplaintComment(id={self.id}, complaint_id={self.complaint_id})>"

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Department(id={self.id}, name={self.name})>"
