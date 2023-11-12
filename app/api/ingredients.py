from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from sqlmodel.sql.expression import select

from app.api.util import get_session
from app.models.ingredient import Ingredient, IngredientRead
from app.models.ingredient_nutrient_link import IngredientNutrientLink
from app.models.nutrient import Nutrient

router = APIRouter()


@router.get("/ingredients/{ingredient_id}")
def get_ingredient(
    ingredient_id: int, session: Session = Depends(get_session)
) -> Ingredient:
    return session.get(Ingredient, ingredient_id)


@router.get("/ingredients")
def get_ingredients(
    session: Session = Depends(get_session),
    nutrients: Annotated[list[str] | None, Query()] = None,
) -> list[IngredientRead]:
    statement = select(Ingredient).order_by(Ingredient.name)

    if nutrients is not None:
        statement = statement.join(
            IngredientNutrientLink,
            Ingredient.id == IngredientNutrientLink.ingredient_id,
        ).join(Nutrient, IngredientNutrientLink.nutrient_id == Nutrient.id)

        statements_to_intersect = []

        for nutrient in nutrients:
            statements_to_intersect.append(statement.where(Nutrient.name == nutrient))

        statement = statements_to_intersect[0].intersect_all(
            *statements_to_intersect[1:]
        )

    ingredients = session.exec(statement).all()

    return ingredients


@router.post("/ingredients", status_code=201)
def add_ingredient(
    ingredient: Ingredient, session: Session = Depends(get_session)
) -> Ingredient:
    session.add(ingredient)

    session.commit()
    session.refresh(ingredient)

    return ingredient
