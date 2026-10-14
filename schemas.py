
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


Priority = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
TicketStatus = Literal["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"]


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    role: str = Field(default="USER", min_length=1, max_length=30)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value.strip()

    @field_validator("role")
    @classmethod
    def validate_role(cls, value):
        if not value.strip():
            raise ValueError("Role cannot be empty")
        return value.strip().upper()


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    priority: Priority = "MEDIUM"
    user_id: int = Field(gt=0)

    @field_validator("title", "description")
    @classmethod
    def validate_text(cls, value):
        if not value.strip():
            raise ValueError("Text cannot be empty")
        return value.strip()


class TicketAssign(BaseModel):
    assigned_to: int = Field(gt=0)


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketPriorityUpdate(BaseModel):
    priority: Priority


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: Priority
    status: TicketStatus
    user_id: int
    assigned_to: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketListResponse(BaseModel):
    page: int
    limit: int
    total: int
    tickets: list[TicketResponse]


class CommentCreate(BaseModel):
    user_id: int = Field(gt=0)
    comment: str = Field(min_length=1)

    @field_validator("comment")
    @classmethod
    def validate_comment(cls, value):
        if not value.strip():
            raise ValueError("Comment cannot be empty")
        return value.strip()


class CommentResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    comment: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketSummary(BaseModel):
    total_tickets: int
    open: int
    in_progress: int
    resolved: int
    closed: int
    critical: int
