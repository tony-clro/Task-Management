from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
    """Schema for standard HTTP error responses."""
    detail: str = Field(..., description="Human-readable explanation of the error")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"detail": "Task with ID 999 not found"}
        }
    )


class TaskBase(BaseModel):
    """Base Pydantic schema with shared attributes for Task models."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="The title of the task",
        examples=["Complete FastAPI Tutorial"],
    )
    description: str | None = Field(
        default=None,
        description="Detailed description of the task",
        examples=["Build and test a clean REST API using FastAPI and SQLAlchemy"],
    )


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Build Task API",
                "description": "Implement CRUD endpoints and test suite",
            }
        }
    )


class TaskUpdate(BaseModel):
    """Schema for updating an existing task. All fields are optional."""
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="The title of the task",
        examples=["Build Refactored Task API"],
    )
    description: str | None = Field(
        default=None,
        description="Detailed description of the task",
        examples=["Updated task details"],
    )
    is_completed: bool | None = Field(
        default=None,
        description="Completion status of the task",
        examples=[True],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Updated Task Title",
                "description": "Updated task description text",
                "is_completed": True,
            }
        }
    )


class TaskStatusUpdate(BaseModel):
    """Schema for marking a task as completed or toggling completion status."""
    is_completed: bool = Field(..., description="Completion status of the task", examples=[True])


class TaskResponse(TaskBase):
    """Schema for serializing a task in API responses."""
    id: int = Field(..., description="Unique integer ID of the task", examples=[1])
    is_completed: bool = Field(..., description="Completion status", examples=[False])
    created_at: datetime = Field(..., description="Timestamp when task was created")
    updated_at: datetime = Field(..., description="Timestamp when task was last updated")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Complete FastAPI Tutorial",
                "description": "Build and test a clean REST API using FastAPI and SQLAlchemy",
                "is_completed": False,
                "created_at": "2026-09-30T02:00:00Z",
                "updated_at": "2026-09-30T02:00:00Z",
            }
        },
    )
