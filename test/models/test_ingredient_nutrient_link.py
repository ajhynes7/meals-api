from sqlmodel import Session

from app.models.ingredient import Ingredient
from app.models.ingredient_nutrient_link import IngredientNutrientLink
from app.models.nutrient import Nutrient


def test_ingredient_with_multiple_nutrients(session: Session):
    ingredient = Ingredient(name="Chickpeas")

    nutrients = [Nutrient(name=name) for name in ["Vitamin B6", "Iron", "Magnesium"]]

    session.add(ingredient)
    session.add_all(nutrients)
    session.commit()

    for nutrient in nutrients:
        link = IngredientNutrientLink(
            ingredient_id=ingredient.id, nutrient_id=nutrient.id
        )
        session.add(link)

    assert ingredient.nutrients == nutrients


def test_nutrient_in_multiple_ingredients(session: Session):
    nutrient = Nutrient(name="Vitamin")

    ingredients = [Ingredient(name=name) for name in ["Orange", "Lemon"]]

    session.add(nutrient)
    session.add_all(ingredients)
    session.commit()

    for ingredient in ingredients:
        link = IngredientNutrientLink(
            ingredient_id=ingredient.id, nutrient_id=nutrient.id
        )
        session.add(link)

    assert nutrient.ingredients == ingredients
