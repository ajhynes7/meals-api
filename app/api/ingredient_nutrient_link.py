from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.util import get_session
from app.models.ingredient_nutrient_link import IngredientNutrientLink

router = APIRouter()


@router.post("/ingredient-nutrient", status_code=201)
def add_ingredient_nutrient_link(
    ingredient_nutrient_link: IngredientNutrientLink,
    session: Session = Depends(get_session),
) -> IngredientNutrientLink:
    session.add(ingredient_nutrient_link)
    session.commit()

    return ingredient_nutrient_link
