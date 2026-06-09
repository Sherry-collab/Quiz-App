from fastapi import FastAPI

import database
import models
from routers import authetication, quiz

# Create tables on startup (no-op if they already exist).
models.Base.metadata.create_all(bind=database.engine)

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Register a user and obtain a JWT access token.",
    },
    {
        "name": "Quizzes",
        "description": "Quiz endpoints. **Protected** — require a valid bearer token.",
    },
]

app = FastAPI(
    title="Quiz App API",
    description=(
        "A simple quiz API with JWT authentication.\n\n"
        "**How to authorize in Swagger:**\n"
        "1. `POST /register` to create a user.\n"
        "2. Click the **Authorize** button (top right) and log in with that "
        "user's email (as username) and password.\n"
        "3. Call the protected `/quizzes` endpoints."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
)

app.include_router(authetication.router)
app.include_router(quiz.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "docs": "/docs"}
