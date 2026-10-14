
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import CommentCreate, CommentResponse
from services import add_comment_service, get_comments_service

router = APIRouter(prefix="/tickets", tags=["Ticket Comments"])


@router.post(
    "/{ticket_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a comment to a ticket",
    description="Rejects comments for closed or non-existing tickets."
)
def add_comment(
    ticket_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db)
):
    return add_comment_service(db, ticket_id, data)


@router.get(
    "/{ticket_id}/comments",
    response_model=list[CommentResponse],
    summary="Get ticket comments"
)
def get_ticket_comments(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    return get_comments_service(db, ticket_id)
