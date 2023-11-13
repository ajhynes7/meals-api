from fastapi import FastAPI

from app.api import ingredient_nutrient_link, ingredients, meals, nutrients

app = FastAPI()


for module in [meals, ingredients, nutrients, ingredient_nutrient_link]:
    app.include_router(module.router)
