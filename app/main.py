from fastapi import FastAPI

from app.api import ingredients, meals

app = FastAPI()


for module in [
    meals,
    ingredients,
]:
    app.include_router(module.router)
