from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, utils
from typing import Optional, List
from ..schemas import PostCreate, PostBase, Post, UserCreate, UserResponse
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


# USER ROUTES
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    # Refresh to get the new user as a response
    db.refresh(new_user)

    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user
