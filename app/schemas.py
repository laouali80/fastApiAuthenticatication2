from pydantic import BaseModel
from typing import Optional
from enum import Enum


class UserLevel(str, Enum):
    user = "user"
    admin = "admin"


class UserBase(BaseModel):
    firstName: str
    lastName: str
    email:str
    disabled: bool = False
    level: UserLevel = UserLevel.user



class UserIn(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: int
    
    class Config:
        orm_mode = True

    
class UserInDB(UserInDBBase):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


