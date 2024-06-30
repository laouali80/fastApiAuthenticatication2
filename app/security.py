from datetime import datetime, timedelta
from jose import JWTError, jwt

# HARSHING PASSWORD
from passlib.context import CryptContext
from dotenv import load_dotenv
import os


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Creaate/Generate an access token to a user."""
    
    # copy the user data
    to_encode = data.copy()

    # if there is a diff btw the currrent time and when we want the token to expire 
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 15)

    # to update our user dict and add "exp" propriety with a expire time 
    to_encode.update({"exp":expire})

    # generate an access token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    #  return the token
    return encoded_jwt

