
from pydantic import BaseModel

class SignInRequest(BaseModel):
    email: str     
    password: str

class SignUpRequest(BaseModel):
    username: str
    email:str
    password: str

class UserResponse(BaseModel):
    status : int
    Message: str


  