
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    role = Column(String(30), default="USER", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    created_tickets = relationship(
        "Ticket",
        foreign_keys="Ticket.user_id",
        back_populates="creator"
    )

    assigned_tickets = relationship(
        "Ticket",
        foreign_keys="Ticket.assigned_to",
        back_populates="assignee"
    )

    comments = relationship("TicketComment", back_populates="user")


class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        UniqueConstraint("id", name="uq_ticket_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(20), default="MEDIUM", nullable=False)
    status = Column(String(20), default="OPEN", nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow, nullable=False
    )

    creator = relationship(
        "User", foreign_keys=[user_id],
        back_populates="created_tickets"
    )

    assignee = relationship(
        "User", foreign_keys=[assigned_to],
        back_populates="assigned_tickets"
    )

    comments = relationship(
        "TicketComment",
        back_populates="ticket",
        cascade="all, delete-orphan"
    )


class TicketComment(Base):
    __tablename__ = "ticket_comments"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(
        Integer, ForeignKey("tickets.id"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    ticket = relationship("Ticket", back_populates="comments")
    user = relationship("User", back_populates="comments")
