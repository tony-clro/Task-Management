from app.models import Task


def test_create_task_in_db(db_session):
    # Verify table initialization and model insertion
    task = Task(title="Test Task", description="Testing DB initialization", is_completed=False)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.id is not None
    assert task.title == "Test Task"
    assert task.description == "Testing DB initialization"
    assert task.is_completed is False
    assert task.created_at is not None
    assert task.updated_at is not None
