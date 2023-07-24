# SQL Alchemy
from sqlalchemy import Boolean, Column, Integer, String, DateTime
# App
from app.db.session import Base


class User(Base):

    __tablename__ = "USERS"
    # ID auto-generated
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    # Required fields
    name = Column(String(50), nullable=False)
    username = Column(String(20), unique=True, index=True, nullable=False)
    # Auto-generated
    hashed_password = Column(String(30), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=None)
    deleted_at = Column(DateTime(timezone=True), default=None)
