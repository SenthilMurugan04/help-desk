
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    TicketCreate, TicketAssign, TicketStatusUpdate,
    TicketPriorityUpdate, TicketResponse,
    TicketListResponse, TicketSummary
)
from services import (
    create_ticket_service,
    assign_ticket_service,
    update_status_service,
    update_priority_service,
    list_tickets_service,
    ticket_summary_service
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a ticket",
    description="Creates a ticket with default status OPEN."
)
def create_ticket(data: TicketCreate, db: Session = Depends(get_db)):
    return create_ticket_service(db, data)


@router.put(
    "/{ticket_id}/assign",
    response_model=TicketResponse,
    summary="Assign a ticket"
)
def assign_ticket(
    ticket_id: int,
    data: TicketAssign,
    db: Session = Depends(get_db)
):
    return assign_ticket_service(db, ticket_id, data.assigned_to)


@router.put(
    "/{ticket_id}/status",
    response_model=TicketResponse,
    summary="Update ticket status",
    description="Only valid sequential status transitions are allowed."
)
def update_status(
    ticket_id: int,
    data: TicketStatusUpdate,
    db: Session = Depends(get_db)
):
    return update_status_service(db, ticket_id, data.status)


@router.put(
    "/{ticket_id}/priority",
    response_model=TicketResponse,
    summary="Update ticket priority"
)
def update_priority(
    ticket_id: int,
    data: TicketPriorityUpdate,
    db: Session = Depends(get_db)
):
    return update_priority_service(db, ticket_id, data.priority)


@router.get(
    "/summary",
    response_model=TicketSummary,
    summary="Get ticket summary",
    description="Returns ticket counts calculated from the database."
)
def get_ticket_summary(db: Session = Depends(get_db)):
    return ticket_summary_service(db)


@router.get(
    "",
    response_model=TicketListResponse,
    summary="List and filter tickets",
    description="Supports status, priority, assignee, and pagination."
)
def list_tickets(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    status_filter: Annotated[
        str | None,
        Query(alias="status", pattern="^(OPEN|IN_PROGRESS|RESOLVED|CLOSED)$")
    ] = None,
    priority: Annotated[
        str | None,
        Query(pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    ] = None,
    assigned_to: Annotated[int | None, Query(ge=1)] = None,
    db: Session = Depends(get_db)
):
    return list_tickets_service(
        db=db,
        page=page,
        limit=limit,
        status=status_filter,
        priority=priority,
        assigned_to=assigned_to
    )
