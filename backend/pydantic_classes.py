from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

class TimeOffStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

############################################
# Classes are defined here
############################################
class TimeOffRequestCreate(BaseModel):
    approvedAt: Optional[datetime] = None
    endDate: date
    reason: str
    startDate: date
    status: TimeOffStatus
    submittedAt: datetime
    approvedBy: Optional[int] = None  # N:1 Relationship (optional)
    requester: int  # N:1 Relationship (mandatory)


class EmployeeCreate(BaseModel):
    email: str
    hiredDate: date
    name: str
    position: str
    manager: Optional[int] = None  # N:1 Relationship (optional)
    timeOffRequests: Optional[List[int]] = None  # 1:N Relationship


class ManagerCreate(EmployeeCreate):
    department: str
    approvedRequests: Optional[List[int]] = None  # 1:N Relationship
    teamMembers: Optional[List[int]] = None  # 1:N Relationship


