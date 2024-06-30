from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import auth, models, schemas, security
from app.db import get_db


router = APIRouter()


@router.post("/", response_model=schemas.UserInDBBase)
async def register(user_in: schemas.UserIn, db: Session = Depends(get_db)):
    db_user = auth.get_user(db, username=user_in.firstName)

    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registerd.")
    
    db_user = db.query(models.User).filter(models.User.email == user_in.email).first()

    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registerd.")
    
    hashed_password = security.get_password_hash(user_in.password)

    db_user = models.User(
        **user_in.dict(exclude={"password"}), hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = auth.get_user(db, username=form_data.username)
    if not user or not security.pwd_context.verify(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.firstName}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/conversation")
async def read_conversation(
    current_user: schemas.UserInDB = Depends(auth.get_current_active_user)
):
    return {
        "conversation": "Yessssss",
        "current_user": current_user.firstName
    }



# @router.get("/users/me/")
# async def read_users_me(current_user: User = Depends(get_current_active_user)) -> User:
#     return current_user


# @router.get("/users/me/items")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{
#         "item_id":1,
#         "owner":current_user
#         }]
