from sqlalchemy import select
from passlib.context import CryptContext
from app.models.user import User
from fastapi import HTTPException
from app.utils.security import create_access_token

from sqlalchemy.orm import  Session
from .schema import SignUpRequest , SignInRequest ,UserResponse


pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=12)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def sign_up(payload: SignUpRequest, db: Session) -> UserResponse:
    existing = db.scalars(select(User).where(User.email == payload.email)).first()

    if existing:
        raise HTTPException(status_code=500, detail="SomeThing Went Wrong")

    new_user = User(
        username=payload.username,
        email=payload.email,
        password=hash_password(payload.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(status=201 , Message="Created Succesfully" )


# service.py


def sign_in(payload: SignInRequest, db: Session) -> UserResponse:
    existing = db.scalars(select(User).where(User.email == payload.email)).first()

    if not existing or not pwd_context.verify(payload.password, existing.password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    
    return create_access_token({"sub":existing.id , "email": existing.email})

