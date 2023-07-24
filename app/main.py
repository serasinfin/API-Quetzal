# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# App
from app.core.config import settings
from app.api.routes import api_router
from app.db.init_db import init_db

# Init DB
init_db()
# Init APP
app = FastAPI(title=settings.PROJECT_NAME)

# Allow all origins = ["*"]
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router)
