from fastapi import APIRouter
from app.database import tasks_collection

router = APIRouter()

@router.post("/")
def create_task(task: dict):
    tasks_collection.insert_one(task)
    return {"message": "Task created"}

@router.get("/")
def get_tasks():
    return list(tasks_collection.find({}, {"_id": 0}))