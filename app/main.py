from fastapi import FastAPI
from backend.app.routes import chat, user, analytic

app = FastAPI(title="SHA Chatbot API", version="1.0")

app.include_router(chat.router, prefix="", tags=["Chatbot"])
app.include_router(user.router, prefix="", tags=["Authentication"])
app.include_router(analytic.router, prefix="", tags=["Analytics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SHA Chatbot API"}