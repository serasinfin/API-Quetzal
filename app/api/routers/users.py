# Python
# FastAPI
from fastapi import APIRouter, Depends, HTTPException, Path, Body
# SQL Alchemy
from sqlalchemy.orm import Session
# Starlette
from starlette import status
# App
from app import schemas, crud
from app.api import jwt
from app.db.get_db import get_db

router = APIRouter()


@router.get(
    path="/",
    description="Obtiene todos los usuarios.",
    status_code=status.HTTP_200_OK,
)
async def get_all(
        skip: int = 0,
        limit: int = 1000,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(jwt.get_current_user)
):
    users = crud.user.get_multi(db=db, skip=skip, limit=limit)
    return [schemas.User.model_validate(u) for u in users]


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DefaultMessage,
)
async def create(
        request: schemas.UserCreate = Body(...),
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(jwt.get_current_user)
) -> any:
    user = crud.user.get_by_username(db=db, username=request.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya existe."
        )
    if crud.user.create(db=db, obj_in=request):
        return {"message": "Usuario creado exitosamente."}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Ocurrio un error y no se guardo el usuario."
    )


@router.put(
    path="/id/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.DefaultMessage,
    description="Actualiza un usuario por su ID."
)
async def update(
        user_id: int = Path(..., gt=0),
        request: schemas.UserUpdate = Body(...),
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(jwt.get_current_user)
) -> any:
    user = crud.user.get_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario con ese ID no existe."
        )
    if user.username != request.username:
        user = crud.user.get_by_username(db=db, username=request.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya existe."
            )
    if crud.user.update(db=db, user_id=user_id, obj_in=request):
        return {"message": "Usuario actualizado exitosamente."}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrio un error y no se actualizo el usuario."
        )


@router.put(
    path="/password-update/id/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.DefaultMessage,
    description="Actualiza la contraseña de un usuario por su ID."
)
async def update_password(
        user_id: int = Path(..., gt=0),
        request: schemas.UserPasswordUpdate = Body(...),
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(jwt.get_current_user)
) -> any:
    user = crud.user.get_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario con ese ID no existe."
        )
    crud.user.update_password(db=db, user_id=user_id, obj_in=request)
    return {"message": "Contraseña actualizada exitosamente."}


@router.delete(
    path="/id/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.DefaultMessage,
    description="Elimina un usuario por su ID."
)
async def delete(
        user_id: int = Path(..., gt=0),
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(jwt.get_current_user)
) -> any:
    user = crud.user.get_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario con ese ID no existe."
        )
    if not user.is_active:
        if user.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya esta eliminado."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario esta inactivo."
            )
    if crud.user.delete(db=db, user_id=user_id):
        return {"message": "Usuario eliminado exitosamente."}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrio un error y no se elimino el usuario."
        )
