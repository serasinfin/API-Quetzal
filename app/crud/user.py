# Python
# SQL Alchemy
from sqlalchemy import asc
from sqlalchemy.orm import Session
# App
from app.schemas import UserCreate, UserUpdate, UserPasswordUpdate
from app.models.user import User
from app.core.security import get_hashed_password
from app.utility.time import today_now
from .base import CRUDBase


class CRUDUser(CRUDBase):
    @classmethod
    def create(
            cls, db: Session, *, obj_in: UserCreate
    ) -> User:
        db_obj = User(
            name=obj_in.name,
            username=obj_in.username,
            hashed_password=get_hashed_password(obj_in.password),
            created_at=today_now()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def update(
            cls, *, db: Session, user_id: int, obj_in: UserUpdate
    ) -> bool:
        db_obj = {
            'name': obj_in.name,
            'username': obj_in.username,
            'updated_at': today_now()
        }
        q = db.query(User).filter(User.id == user_id).update(db_obj)
        db.commit()
        if q:
            return True
        return False

    @classmethod
    def update_password(
            cls, *, db: Session, user_id: int, obj_in: UserPasswordUpdate
    ) -> bool:
        db_obj = {
            'hashed_password': get_hashed_password(obj_in.password),
        }
        db.query(User).filter(User.id == user_id).update(db_obj)
        db.commit()
        return True

    @classmethod
    def delete(
            cls, *, db: Session, user_id: int
    ) -> bool:
        db_obj = {
            'is_active': False,
            'deleted_at': today_now(),
        }
        db.query(User).filter(User.id == user_id).update(db_obj)
        db.commit()
        return True

    @classmethod
    def get_by_username(
            cls, *, db: Session, username: str
    ) -> User:
        return db.query(User).filter(User.username == username).first()

    @classmethod
    def get_by_id(
            cls, *, db: Session, user_id: int
    ) -> User:
        return db.query(User).filter(User.id == user_id).first()

    @classmethod
    def get_multi(
            cls, *, db: Session, skip: int = 0, limit: int = 100
    ) -> list[User]:
        return db.query(User).order_by(asc(User.id)).offset(skip).limit(limit).all()


user = CRUDUser()
