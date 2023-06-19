from fastapi import FastAPI

from app.api import meals

app = FastAPI()


for module in [
    meals,
]:
    app.include_router(module.router)
