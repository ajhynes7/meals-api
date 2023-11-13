from fastapi import FastAPI

from app.api import ingredients, meals, nutrients

app = FastAPI()


for module in [meals, ingredients, nutrients]:
    app.include_router(module.router)
