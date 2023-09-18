# fastAPI
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
# SQL Alchemy
from sqlalchemy.orm import Session
# Starlette
from starlette import status

# App
from app import schemas, crud
from app.core.security import verify_password, create_access_token, decode_token
from app.db.get_db import get_db

router = APIRouter()


@router.post(
	path="/login",
	response_model=schemas.Token,
	status_code=status.HTTP_202_ACCEPTED
)
def login(
		request: OAuth2PasswordRequestForm = Depends(),
		raw_request: Request = None,
		db: Session = Depends(get_db)
) -> any:
	user = crud.user.get_by_username(db=db, username=request.username)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Usuario o contraseña incorrectos",
		)
	if not user.is_active:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Usuario inactivo",
		)
	if not verify_password(
			plain_password=request.password,
			hashed_password=user.hashed_password
	):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Usuario o contraseña incorrectos",
		)

	access_token = create_access_token(
		data={
			"sub": user.username,
		}
	)
	# SAVE VALID TOKEN
	token_active = crud.auth.get_valid_token(db=db, username=user.username)
	user_ip = raw_request.client.host
	if token_active:
		crud.auth.update_valid_token(db=db, username=token_active.username, token=access_token, user_ip=user_ip)
	else:
		crud.auth.create_valid_token(db=db, username=user.username, token=access_token, user_ip=user_ip)
	token = {
		"user_data": {
			"id": user.id,
			"name": user.name,
			"username": user.username,
		},
		"access_token": access_token,
		"token_type": "bearer"
	}
	return token


@router.post(
	path="/me",
	response_model=schemas.Token,
	status_code=status.HTTP_200_OK
)
def me(
		access_token: str
) -> any:
	access_token = access_token.replace('"', '')
	decoded_token = decode_token(access_token)
	if not decoded_token:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Token inválido",
		)
	token = {
		"user_data": {
			"id": decoded_token.get("id"),
			"name": decoded_token.get("name"),
			"username": decoded_token.get("username"),
		},
		"access_token": access_token,
		"token_type": "bearer"
	}
	return token
