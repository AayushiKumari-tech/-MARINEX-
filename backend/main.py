from fastapi import FastAPI
from app.mission.models import Mission

app = FastAPI(
    title="MARINEX API",
    description="Marine Mission Intelligence & Decision Engine",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "MARINEX API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
@app.post("/mission")
def create_mission(mission: Mission):
    return {
        "message": "Mission received successfully",
        "mission": mission
    }