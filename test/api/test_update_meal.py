from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.ingredient import Ingredient
from app.models.meal import Meal


def test_update_meal_name(session: Session, client: TestClient):
    old_meal_name = "Peanut satay ramen"
    new_meal_name = "Kkanpoong tofu"

    meal = Meal(name=old_meal_name)

    session.add(meal)
    session.commit()

    response = client.patch(
        f"/meals/{meal.id}",
        json={
            "name": new_meal_name,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": meal.id,
        "name": new_meal_name,
        "ingredients": [],
    }

    assert meal.name == new_meal_name


def test_update_meal_ingredients(session: Session, client: TestClient):
    meal = Meal(name="Peanut satay ramen")

    ingredients = [Ingredient(name=name) for name in ["Tofu", "Peanut butter", "Ramen"]]

    session.add(meal)
    session.add_all(ingredients)
    session.commit()

    response = client.patch(
        f"/meals/{meal.id}",
        json={
            "ingredient_names": [ingredient.name for ingredient in ingredients],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": meal.id,
        "name": meal.name,
        "ingredients": [
            {"id": ingredient.id, "name": ingredient.name} for ingredient in ingredients
        ],
    }

    assert meal.ingredients == ingredients


def test_update_meal_with_nonexistent_ingredients(session: Session, client: TestClient):
    meal = Meal(name="Peanut satay ramen")

    ingredients = [Ingredient(name=name) for name in ["Tofu", "Peanut butter", "Ramen"]]

    session.add(meal)
    session.add_all(ingredients)
    session.commit()

    response = client.patch(
        f"/meals/{meal.id}",
        json={
            "ingredient_names": ["Apples"],
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "At least one of these ingredients does not exist."
    }
