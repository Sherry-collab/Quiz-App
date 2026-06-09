from fastapi import APIRouter, Depends, HTTPException, status

import models
import schemas
from oauth2 import get_current_user

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

# Dummy in-memory data — stands in for a real quiz table for now.
_DUMMY_QUIZZES = [
    {
        "id": 1,
        "title": "Python Basics",
        "questions": [
            {
                "id": 1,
                "text": "What keyword defines a function in Python?",
                "options": ["func", "def", "function", "lambda"],
            },
            {
                "id": 2,
                "text": "Which type is immutable?",
                "options": ["list", "dict", "tuple", "set"],
            },
        ],
    },
    {
        "id": 2,
        "title": "FastAPI Fundamentals",
        "questions": [
            {
                "id": 1,
                "text": "Which decorator handles a POST request?",
                "options": ["@app.get", "@app.post", "@app.put", "@app.delete"],
            },
        ],
    },
]


@router.post("/", response_model=schemas.Quiz, status_code=status.HTTP_201_CREATED)
def create_quiz(
    request: schemas.QuizCreate,
    current_user: models.User = Depends(get_current_user),
):
    """Create a quiz. Only users with the **teacher** role are allowed."""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can create quizzes",
        )

    new_id = max((q["id"] for q in _DUMMY_QUIZZES), default=0) + 1
    quiz = {
        "id": new_id,
        "title": request.title,
        "questions": [
            {"id": i + 1, "text": q.text, "options": q.options}
            for i, q in enumerate(request.questions)
        ],
    }
    _DUMMY_QUIZZES.append(quiz)
    return quiz


@router.get("/", response_model=list[schemas.Quiz])
def list_quizzes(current_user: models.User = Depends(get_current_user)):
    """List all quizzes. Requires a valid bearer token."""
    return _DUMMY_QUIZZES


@router.get("/{quiz_id}", response_model=schemas.Quiz)
def get_quiz(
    quiz_id: int,
    current_user: models.User = Depends(get_current_user),
):
    """Fetch a single quiz by id. Requires a valid bearer token."""
    for quiz in _DUMMY_QUIZZES:
        if quiz["id"] == quiz_id:
            return quiz
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Quiz {quiz_id} not found",
    )
