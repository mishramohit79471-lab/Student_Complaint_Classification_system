from pydantic import BaseModel
from datetime import datetime

class DepartmentBase(BaseModel):
    name: str
    description: str = ""

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
