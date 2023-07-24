# Python
from datetime import datetime
# Pydantic
from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(..., min_length=4, max_length=20, description="Nombre de usuario para iniciar sesión. 4-20 caracteres")
    name: str = Field(..., min_length=2, max_length=50, description="Nombre completo del usuario 2-50 caracteres")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=30)


class UserUpdate(UserBase):
    pass


class UserPasswordUpdate(BaseModel):
    password: str = Field(..., min_length=8, max_length=30)


class UserInDBBase(UserBase):
    id: int
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None
    deleted_at: datetime | None


class UserInDB(UserInDBBase):
    hashed_password: str


class User(UserInDBBase):
    model_config = ConfigDict(from_attributes=True)
    pass
