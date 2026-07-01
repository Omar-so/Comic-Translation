from fastapi import APIRouter, Depends ,Response
from sqlalchemy.orm import Session
from app.models.database import get_db
from .schema import SignInRequest , UserResponse , SignUpRequest , UserResponse
from .service import sign_up, sign_in
from app.config import settings

router = APIRouter(
    prefix="/Auth",
    tags=["auth"],
    dependencies=[Depends(get_db)],
)

@router.post("/signin")
async def signin_endpoint(payload: SignInRequest, response: Response, db: Session = Depends(get_db)):
    token = sign_in(payload, db) 

    response.set_cookie(
        key="Token_X",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=settings.SESSION_EXPIRE_SECONDS
    )
    return {"message": "signed in"}



@router.post("/SignUp", tags=["users"])
def sign_up(payload: SignUpRequest ,db: Session = Depends(get_db)):
    return  sign_up(payload, db)


