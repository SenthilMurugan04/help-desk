
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from models import User, Ticket, TicketComment
from crud import (
    get_user, get_ticket, get_user_by_email,
    create_user, create_ticket, save_ticket,
    create_comment, get_comments
)


ALLOWED_TRANSITIONS = {
    "OPEN": ["IN_PROGRESS"],
    "IN_PROGRESS": ["RESOLVED"],
    "RESOLVED": ["CLOSED"],
    "CLOSED": []
}


def create_user_service(db: Session, data):
    if get_user_by_email(db, str(data.email)):
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    try:
        return create_user(db, data)
    except Exception:
        db.rollback()
        raise


def create_ticket_service(db: Session, data):
    if not get_user(db, data.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    try:
        return create_ticket(db, data)
    except Exception:
        db.rollback()
        raise


def assign_ticket_service(db: Session, ticket_id: int, assigned_to: int):
    ticket = get_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket.status == "CLOSED":
        raise HTTPException(
            status_code=400,
            detail="Closed tickets cannot be assigned"
        )

    if not get_user(db, assigned_to):
        raise HTTPException(status_code=404, detail="Assignee not found")

    ticket.assigned_to = assigned_to
    return save_ticket(db, ticket)


def update_status_service(db: Session, ticket_id: int, new_status: str):
    ticket = get_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket.status == "CLOSED":
        raise HTTPException(
            status_code=400,
            detail="Closed tickets cannot be modified"
        )

    if new_status not in ALLOWED_TRANSITIONS[ticket.status]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transition: {ticket.status} to {new_status}"
        )

    ticket.status = new_status
    return save_ticket(db, ticket)


def update_priority_service(db: Session, ticket_id: int, priority: str):
    ticket = get_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket.status == "CLOSED":
        raise HTTPException(
            status_code=400,
            detail="Closed tickets cannot be modified"
        )

    ticket.priority = priority
    return save_ticket(db, ticket)


def list_tickets_service(
    db: Session,
    page: int,
    limit: int,
    status=None,
    priority=None,
    assigned_to=None
):
    query = db.query(Ticket)

    if status:
        query = query.filter(Ticket.status == status)

    if priority:
        query = query.filter(Ticket.priority == priority)

    if assigned_to is not None:
        query = query.filter(Ticket.assigned_to == assigned_to)

    total = query.count()

    tickets = (
        query.order_by(Ticket.id.asc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "tickets": tickets
    }


def add_comment_service(db: Session, ticket_id: int, data):
    ticket = get_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket.status == "CLOSED":
        raise HTTPException(
            status_code=400,
            detail="Closed tickets cannot receive comments"
        )

    if not get_user(db, data.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    try:
        return create_comment(db, data, ticket_id)
    except Exception:
        db.rollback()
        raise


def get_comments_service(db: Session, ticket_id: int):
    if not get_ticket(db, ticket_id):
        raise HTTPException(status_code=404, detail="Ticket not found")

    return get_comments(db, ticket_id)


def ticket_summary_service(db: Session):
    total = db.query(func.count(Ticket.id)).scalar() or 0

    counts = dict(
        db.query(Ticket.status, func.count(Ticket.id))
        .group_by(Ticket.status)
        .all()
    )

    critical = (
        db.query(func.count(Ticket.id))
        .filter(Ticket.priority == "CRITICAL")
        .scalar()
        or 0
    )

    return {
        "total_tickets": total,
        "open": counts.get("OPEN", 0),
        "in_progress": counts.get("IN_PROGRESS", 0),
        "resolved": counts.get("RESOLVED", 0),
        "closed": counts.get("CLOSED", 0),
        "critical": critical
    }
