from fastapi import APIRouter
from app.database import users_collection

router = APIRouter()

@router.post("/")
def create_user(user: dict):
    users_collection.insert_one(user)
    return {"message": "User created"}
