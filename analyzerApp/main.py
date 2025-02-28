from fastapi import FastAPI
from analyzerApp.routes import router

app = FastAPI(title="Autonomous Code Review Agent")
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello to the application, please use Postman or other API platform for testing! Browser API access has been disabled due to DDoS concerns."}