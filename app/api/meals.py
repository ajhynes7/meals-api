from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from sqlmodel import Session
from sqlmodel.sql.expression import select

from app.api.util import get_session
from app.models.meal import Meal
from app.models.ingredient import Ingredient
from typing import Annotated
from app.models.meal_ingredient_link import MealIngredientLink
from app.models.meal import MealUpdate
from app.models.meal import MealReadWithIngredients

router = APIRouter()


@router.get("/meals/{meal_id}", response_model=MealReadWithIngredients)
def read_meal(
    meal_id: int,
    session: Session = Depends(get_session),
):
    return session.get(Meal, meal_id)


@router.get("/meals")
def read_meals(
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


@router.post("/meals", status_code=201)
def add_meal(meal: Meal, session: Session = Depends(get_session)):
    session.add(meal)

    try:
        session.commit()
    except IntegrityError as error:
        if isinstance(error.orig, UniqueViolation):
            raise HTTPException(status_code=409, detail="This name already exists.")

    session.refresh(meal)

    return meal


@router.patch(
    "/meals/{meal_id}", status_code=200, response_model=MealReadWithIngredients
)
def update_meal(
    meal_id: int, meal_update: MealUpdate, session: Session = Depends(get_session)
):
    meal = session.get(Meal, meal_id)

    if meal_update.name:
        meal.name = meal_update.name

    if meal_update.ingredient_ids:
        ingredients = session.exec(
            select(Ingredient).where(Ingredient.id.in_(meal_update.ingredient_ids))
        ).all()

        meal.ingredients = ingredients

    session.commit()

    return meal
