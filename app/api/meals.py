from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from sqlmodel.sql.expression import select

from app.api.util import get_session
from app.models.ingredient import Ingredient
from app.models.meal import Meal, MealRead, MealReadWithIngredients, MealUpdate
from app.models.meal_ingredient_link import MealIngredientLink

router = APIRouter()


@router.get("/meals/{meal_id}")
def get_meal(
    meal_id: int,
    session: Session = Depends(get_session),
) -> MealReadWithIngredients:
    meal = session.get(Meal, meal_id)

    if not meal:
        raise HTTPException(status_code=404, detail="This meal does not exist.")

    return meal


@router.get("/meals")
def get_meals(
    session: Session = Depends(get_session),
    ingredients: Annotated[list[str] | None, Query()] = None,
) -> list[MealRead]:
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
def add_meal(meal: Meal, session: Session = Depends(get_session)) -> MealRead:
    session.add(meal)

    try:
        session.commit()
    except IntegrityError as error:
        if isinstance(error.orig, UniqueViolation):
            raise HTTPException(status_code=409, detail="This name already exists.")

    session.refresh(meal)

    return meal


@router.patch("/meals/{meal_id}", status_code=200)
def update_meal(
    meal_id: int, meal_update: MealUpdate, session: Session = Depends(get_session)
) -> MealReadWithIngredients:
    meal = session.get(Meal, meal_id)

    if meal_update.name:
        meal.name = meal_update.name

    if meal_update.source:
        meal.source = meal_update.source

    if meal_update.type:
        meal.type = meal_update.type

    if meal_update.url:
        meal.url = meal_update.url

    if meal_update.ingredient_names:
        ingredients = session.exec(
            select(Ingredient).where(Ingredient.name.in_(meal_update.ingredient_names))
        ).all()

        if len(ingredients) != len(meal_update.ingredient_names):
            raise HTTPException(
                status_code=403,
                detail="At least one of these ingredients does not exist.",
            )

        meal.ingredients = ingredients

    session.commit()

    return meal
