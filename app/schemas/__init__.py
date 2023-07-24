# Pydantic
from pydantic import BaseModel
# App
from .auth import Token, TokenData
from .user import User, UserCreate, UserUpdate, UserPasswordUpdate


class DefaultMessage(BaseModel):
    message: str
