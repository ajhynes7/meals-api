from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.api.util import get_session
from app.models.ingredient import Ingredient
from app.models.ingredient_nutrient_link import (
    IngredientNutrientLink,
    IngredientNutrientLinkbyName,
)
from app.models.nutrient import Nutrient

router = APIRouter()


@router.post("/ingredient-nutrient", status_code=201)
def add_ingredient_nutrient_link(
    ingredient_nutrient_link: IngredientNutrientLink,
    session: Session = Depends(get_session),
) -> IngredientNutrientLink:
    session.add(ingredient_nutrient_link)
    session.commit()

    return ingredient_nutrient_link


@router.post("/ingredient-nutrient/name", status_code=201)
def add_ingredient_nutrient_link_by_name(
    ingredient_nutrient_link_by_name: IngredientNutrientLinkbyName,
    session: Session = Depends(get_session),
) -> IngredientNutrientLink:
    ingredient = session.exec(
        select(Ingredient).where(
            Ingredient.name == ingredient_nutrient_link_by_name.ingredient_name
        )
    ).one()

    nutrient = session.exec(
        select(Nutrient).where(
            Nutrient.name == ingredient_nutrient_link_by_name.nutrient_name
        )
    ).one()

    ingredient_nutrient_link_by_name = IngredientNutrientLink(
        ingredient_id=ingredient.id, nutrient_id=nutrient.id
    )
    session.add(ingredient_nutrient_link_by_name)
    session.commit()

    return ingredient_nutrient_link_by_name
