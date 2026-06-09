from typing import List, Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str


class Login(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


# --- Quiz schemas ---
class Question(BaseModel):
    id: int
    text: str
    options: List[str]


class Quiz(BaseModel):
    id: int
    title: str
    questions: List[Question]
