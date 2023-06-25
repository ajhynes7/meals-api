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

        statements_to_intersect = []

        for ingredient in ingredients:
            statements_to_intersect.append(
                statement.where(Ingredient.name == ingredient)
            )

        statement = statements_to_intersect[0].intersect_all(
            *statements_to_intersect[1:]
        )

    meals = session.exec(statement).all()

    return meals
