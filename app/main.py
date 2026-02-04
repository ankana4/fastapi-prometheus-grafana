from fastapi import FastAPI
from app.routes import users, tasks
from app.metrics import setup_metrics
import logging

app = FastAPI(title="FastAPI Monitoring System")


logging.basicConfig(
    filename="/var/log/app/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

setup_metrics(app)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Monitoring system is running"}

@app.get("/error")
def error():
    logger.error("Something went wrong!")
    return {"error": "oops"}




