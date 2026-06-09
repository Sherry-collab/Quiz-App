from fastapi import FastAPI, Depends, HTTPException
import models, schemas, database
from sqlalchemy.orm import Session

app = FastAPI()

get_db = database.get_db

@app.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == request.email
    ).first()

    if not user:
        raise HTTPException(status_code=404,
                            detail="User not found")

    if user.password != request.password: 
        raise HTTPException(status_code=401,
                            detail="Invalid password")

    return {
        "message": "Login successful",
        "role": user.role
    }

