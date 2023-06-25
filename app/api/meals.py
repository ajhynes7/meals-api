from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from sqlmodel.sql.expression import select

from app.api.util import get_session
from app.models.meal import Meal
from app.models.ingredient import Ingredient
from typing import Annotated
from app.models.meal_ingredient_link import MealIngredientLink

router = APIRouter()


@router.get("/meals")
def get_meals(
    session: Session = Depends(get_session),
    ingredients: Annotated[list[str] | None, Query()] = None,
):
    statement = select(Meal)

    if ingredients is not None:
        statement = statement.join(
            MealIngredientLink, Meal.id == MealIngredientLink.meal_id
        ).join(Ingredient, MealIngredientLink.ingredient_id == Ingredient.id)

        for ingredient in ingredients:
            statement = statement.where(Ingredient.name == ingredient)

    meals = session.exec(statement).all()

    return meals
