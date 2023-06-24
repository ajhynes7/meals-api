from sqlmodel import Session
from app.models.meal import Meal
from app.models.ingredient import Ingredient
from app.models.meal_ingredient_link import MealIngredientLink


def test_meal_with_multiple_ingredients(session: Session):
    meal = Meal(name="Hummus")

    ingredients = [
        Ingredient(name=name)
        for name in ["Chickpeas", "Garlic", "Lemon", "Olive oil", "Tahini"]
    ]

    session.add(meal)
    session.add_all(ingredients)
    session.commit()

    for ingredient in ingredients:
        link = MealIngredientLink(meal_id=meal.id, ingredient_id=ingredient.id)
        session.add(link)

    assert meal.ingredients == ingredients


def test_ingredient_in_multiple_meals(session: Session):
    ingredient = Ingredient(name="Chickpeas")

    meals = [Meal(name=name) for name in ["Hummus", "Falafel"]]

    session.add(ingredient)
    session.add_all(meals)
    session.commit()

    for meal in meals:
        link = MealIngredientLink(meal_id=meal.id, ingredient_id=ingredient.id)
        session.add(link)

    assert ingredient.meals == meals
