from fastapi import FastAPI

app = FastAPI(
    title="StreamHive Recommender Service",
    version="1.0.0"
)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "recommender"}

@app.get("/recommendations")
async def get_recommendations(user_id: int = 1):
    return {
        "user_id": user_id,
        "recommendations": [
            {"id": 101, "title": "Aprende Python desde cero"},
            {"id": 102, "title": "Cómo editar videos rápido"},
            {"id": 103, "title": "Matemática fácil para principiantes"}
        ]
    }
