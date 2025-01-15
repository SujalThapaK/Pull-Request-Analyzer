from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Autonomous Code Review Agent")
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello to the PotpieAI3 team!"}