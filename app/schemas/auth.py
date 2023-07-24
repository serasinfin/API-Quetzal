# Python
from datetime import datetime
# Pydantic
from pydantic import BaseModel


class Token(BaseModel):
	access_token: str
	token_type: str
	user_data: dict


class TokenData(BaseModel):
	username: str


class Login(BaseModel):
	username: str
	password: str


class ValidToken(BaseModel):
	username: str
	token: str = None
	updated_at: datetime = None
