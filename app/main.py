from fastapi import FastAPI
from app.routes import users, tasks
from app.metrics import setup_metrics

app = FastAPI(title="FastAPI Monitoring System")

setup_metrics(app)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

@app.get("/")
def root():
    return {"message": "Monitoring system is running"}



