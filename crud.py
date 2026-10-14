
from sqlalchemy.orm import Session

from models import User, Ticket, TicketComment


# User operations
def create_user(db: Session, data):
    user = User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session):
    return db.query(User).order_by(User.id).all()


# Ticket operations
def get_ticket(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def save_ticket(db: Session, ticket: Ticket):
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def create_ticket(db: Session, data):
    ticket = Ticket(
        title=data.title,
        description=data.description,
        priority=data.priority,
        status="OPEN",
        user_id=data.user_id
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


# Comment operations
def create_comment(db: Session, data, ticket_id: int):
    comment = TicketComment(
        ticket_id=ticket_id,
        user_id=data.user_id,
        comment=data.comment
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments(db: Session, ticket_id: int):
    return (
        db.query(TicketComment)
        .filter(TicketComment.ticket_id == ticket_id)
        .order_by(TicketComment.created_at.asc(), TicketComment.id.asc())
        .all()
    )
