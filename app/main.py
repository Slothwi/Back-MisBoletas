from fastapi import FastAPI
from app.api.v1 import user, product

app = FastAPI()

app.include_router(user.router, prefix="/api/v1")
app.include_router(product.router, prefix="/api/v1")