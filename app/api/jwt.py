# Python
from jose import jwt, JWTError
# FastAPI
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
# SQL Alchemy
from sqlalchemy.orm import Session
# Starlette
from starlette import status

# App
from app import crud, schemas
from app.db.get_db import get_db
from app.core.config import settings
from app.core.security import ALGORITHM
from secrets import compare_digest

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> schemas.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.replace('"', ''), settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.user.get_by_username(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    if user.is_active is False:
        raise credentials_exception

    valid_token = crud.auth.get_valid_token(db=db, username=token_data.username)
    if valid_token is None or not compare_digest(valid_token.token, token.replace('"', '')):
        raise credentials_exception
    return schemas.User.model_validate(user)
