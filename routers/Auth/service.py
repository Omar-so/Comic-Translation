import bcrypt
from sqlalchemy import select
from app.models.user import User
from fastapi import HTTPException
from app.utils.security import create_access_token

from sqlalchemy.orm import Session
from .schema import SignUpRequest, SignInRequest, UserResponse


def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt(rounds=12))
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def sign_up(payload: SignUpRequest, db: Session) -> UserResponse:

    existing = db.scalars(select(User).where(User.email == payload.email)).first()

    if existing:
        raise HTTPException(status_code=500, detail="Try anthor Time!")

    new_user = User(
        name=payload.username,
        email=payload.email,
        password=hash_password(payload.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(status=201, Message="Created Succesfully")

# service.py


def sign_in(payload: SignInRequest, db: Session) -> UserResponse:
    existing = db.scalars(select(User).where(User.email == payload.email)).first()

    if not existing or not verify_password(payload.password, existing.password):
        raise HTTPException(status_code=401, detail="invalid credentials")

    return create_access_token({"sub": str(existing.id), "email": existing.email})