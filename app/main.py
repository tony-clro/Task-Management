from contextlib import asynccontextmanager
from fastapi import FastAPI
from app import models  # noqa: F401 - ensure models are registered with Base.metadata
from app.config import settings
from app.database import engine, Base
from app.routers import tasks


tags_metadata = [
    {
        "name": "Health",
        "description": "API status and health monitoring endpoint.",
    },
    {
        "name": "Tasks",
        "description": "Task management CRUD operations, status updates, and completion filtering.",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables exist on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A clean, beginner-friendly Task Management REST API using FastAPI and SQLAlchemy.",
    version="1.0.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

# Include task router
app.include_router(tasks.router)


@app.get("/", tags=["Health"], summary="Health check endpoint")
def read_root():
    """
    Health check / root endpoint confirming API is up and running.
    """
    return {
        "status": "online",
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs_url": "/docs",
    }
