
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine
import models

from routers import users, tickets, comments


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Helpdesk Ticket Management API",
    description=(
        "REST API for managing helpdesk users, tickets, "
        "assignments, status transitions, priorities, comments, "
        "filters, pagination, and ticket summaries."
    ),
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(users.router)
app.include_router(tickets.router)
app.include_router(comments.router)


@app.get("/", tags=["Home"], summary="API welcome")
def home():
    return {
        "message": "Welcome to the Helpdesk Ticket Management API",
        "documentation": "/docs"
    }
