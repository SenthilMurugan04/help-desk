
# Helpdesk Ticket Management API

## Project Description

The Helpdesk Ticket Management API is a RESTful application
developed using Python, FastAPI, SQLAlchemy, Pydantic, and SQLite.

It allows users to create and manage helpdesk tickets, assign
tickets to employees, update ticket status and priority, add
comments, filter ticket records, and view ticket statistics.

## Technologies

- Python
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic
- Swagger/OpenAPI

## Installation

Install the required dependencies:

    python -m pip install -r requirements.txt

## Run the Application

    uvicorn main:app --reload

## API Documentation

Swagger UI:

    http://127.0.0.1:8000/docs

OpenAPI JSON:

    http://127.0.0.1:8000/openapi.json

## Main Features

- User creation and duplicate email validation
- Ticket creation and assignment
- Valid ticket status transitions
- Priority management
- Filtering and pagination
- Ticket comments
- Database-driven ticket summary
- SQLAlchemy database relationships
- Pydantic request and response validation
- HTTP exception handling

## Database

SQLite stores data in helpdesk.db in the project directory.
The application creates its tables when it starts.
