from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import database

from database import engine
from src.controllers import auth_controller
from src.controllers import user_controller

app = FastAPI()
app.include_router(auth_controller.router)
app.include_router(user_controller.router)

database.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
