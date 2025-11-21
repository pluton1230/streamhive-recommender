from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import WatchEventDB

# Crear tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StreamHive Recommender Service",
    version="1.0.0"
)

# --------- MODELOS Pydantic ---------

class WatchEvent(BaseModel):
    user_id: int
    video_id: int
    seconds_watched: int

# --------- DEPENDENCIA DB ---------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------- ENDPOINTS ---------

@app.get("/health")
async def health():
    return {"status": "ok", "service": "recommender"}

@app.get("/recommendations")
async def get_recommendations(user_id: int = 1):
    return {
        "user_id": user_id,
        "recommendations": [
            {"id": 101, "title": "Curso rápido de Python"},
            {"id": 202, "title": "Introducción a edición de video"},
            {"id": 303, "title": "Matemática sencilla para principiantes"},
        ]
    }

@app.post("/events/watch")
async def register_watch_event(
    event: WatchEvent,
    db: Session = Depends(get_db)
):
    record = WatchEventDB(
        user_id=event.user_id,
        video_id=event.video_id,
        seconds_watched=event.seconds_watched,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"status": "ok", "id": record.id}
