from fastapi import FastAPI
from app.api.v1 import user

app = FastAPI()

app.include_router(user.router, prefix="/api/v1/user")