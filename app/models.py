from sqlalchemy import Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String, Boolean


from app.db import Base
from app.schemas import UserLevel


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, unique =True, index=True)
    lastName = Column(String, unique =True, index=True)
    email = Column(String, unique=True, index=True)
    disabled = Column(Boolean, default=False)
    level = Column(SQLEnum(UserLevel))
    hashed_password = Column(String)
    
