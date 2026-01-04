from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import Base, engine
from . import schemas, crud, deps
from fastapi.security import OAuth2PasswordRequestForm
from .auth import authenticate_user, create_access_token

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend Data Management System")

@app.get("/")
def root():
    return {"status": "Backend Data Management System is running"}


@app.get("/users", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(deps.get_db)):
    return crud.get_users(db)


@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    return crud.create_user(db, user)


@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(deps.get_db)):
    return crud.update_user(db, user_id, user)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(deps.get_db)):
    crud.delete_user(db, user_id)
    return {"message": "User deleted"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}