from fastapi import Cookie, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.security import decode_access_token
from app.models.database import get_db 
from app.models.user import User 

from jose import JWTError

def get_current_user(
    Token_X: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    if Token_X is None:
        raise HTTPException(status_code=401, detail="not authenticated")
    
    print(Token_X)
    try:
        payload = decode_access_token(Token_X)
    except JWTError as e:
        print(f"JWT Verification Failed: {e}")
        raise HTTPException(status_code=401, detail="invalid or expired token")

    user = db.get(User, int(payload["sub"]))
    if user is None:
        raise HTTPException(status_code=401, detail="user not found")

    return user