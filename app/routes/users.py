from fastapi import APIRouter, HTTPException
from app.database import users_collection

router = APIRouter()

@router.post("/")
def create_user(user: dict):
    try:
        users_collection.insert_one(user)
        return {"message": "User created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="DB error")