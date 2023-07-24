# SQL Alchemy
from sqlalchemy import String, Column, DateTime
# App
from app.db.session import Base


class ValidToken(Base):
    __tablename__ = "VALID_TOKENS"

    username = Column(String, primary_key=True, index=True, nullable=False)
    token = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True, default=None)
    user_ip = Column(String, nullable=True, default=None)
