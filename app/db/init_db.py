# App
from app import models
from .session import engine


def init_db():
	models.Base.metadata.create_all(bind=engine)
