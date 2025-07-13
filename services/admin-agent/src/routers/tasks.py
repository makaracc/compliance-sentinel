"""
Task management endpoints (simplified for testing)
"""

from fastapi import APIRouter
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter()

# In-memory task storage for demo
tasks_db = [
    {"id": 1, "title": "Review GDPR compliance", "status": "Pending", "priority": "High"},
    {"id": 2, "title": "Update privacy policy", "status": "In Progress", "priority": "Medium"},
    {"id": 3, "title": "Conduct security audit", "status": "Completed", "priority": "High"}
]


@router.get("/", summary="List Tasks")
async def list_tasks():
    """Get list of tasks"""
    return tasks_db


@router.get("/{task_id}", summary="Get Task")
async def get_task(task_id: int):
    """Get a specific task by ID"""
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if task:
        return task
    return {"id": task_id, "title": f"Task {task_id}", "status": "Pending", "priority": "Medium"}


@router.post("/", summary="Create Task")
async def create_task(title: str, priority: str = "Medium"):
    """Create a new task"""
    new_task = {
        "id": len(tasks_db) + 1,
        "title": title,
        "status": "Pending",
        "priority": priority
    }
    tasks_db.append(new_task)
    return new_task
