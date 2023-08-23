from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db

from .. import utils, oauth2
from ..schemas import UserLogin
from ..models import User

router = APIRouter(prefix="/api/v1", tags=["Authentication"])
# router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # OAuth2PAsswordRequestForm takes the "email" as username. The form's default must be username.
    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    # GENERATE A TOKEN
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # RETURN A TOKEN
    return {"access_token": access_token, "token_type": "bearer"}
