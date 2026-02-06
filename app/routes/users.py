from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError
from app.database import users_collection
from app.schema.user import UserCreate
from app.metrics import USER_CREATED_TOTAL, USER_CREATE_FAILED_TOTAL
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/")
def create_user(user: UserCreate):
    try:
        exixting_user = users_collection.find_one({"email": user.email})
        if exixting_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
        users_collection.insert_one(user.model_dump())
        USER_CREATED_TOTAL.inc()
        logger.info(f"User created: {user.name}")
        return {"message": "User created"}
    
    except DuplicateKeyError:
        USER_CREATE_FAILED_TOTAL.labels("duplicate_email").inc()
        logger.warning(f"User with email {user.email} already exists")
        if user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
    except HTTPException:
        raise
            
    except Exception as e:
        USER_CREATE_FAILED_TOTAL.labels("internal_server_error").inc()
        logger.exception("Failed to create user")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    
    
@router.get("/")
def get_users():
    logger.info(f"getting all user data")
    return list(users_collection.find({}, {"_id": 0}))