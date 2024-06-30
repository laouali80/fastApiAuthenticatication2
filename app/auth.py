from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import models, schemas, security
from app.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.firstName == username).first()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Authenticate a user token to check if he/she has access."""

    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not validate credentials",
                                           headers={"WWW-Authenticate": "Bearer"}
                                           )

    try:
        # we decode the token to get the username from it
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get('sub')

        # check if there is a username associated with the token
        if username is None:
            raise credential_exception
        
        # we get the token data associated with the username
        token_data = schemas.TokenData(username=username)

    except JWTError:
        raise credential_exception
    
    # make sure that the user is in the database
    user = get_user(db, username=token_data.username)

    if user is None:
        raise credential_exception
    
    return user


