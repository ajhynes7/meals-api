from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.ingredient import Ingredient
from app.models.meal import Meal


def test_update_meal_attributes(session: Session, client: TestClient):
    meal = Meal(name="Kkanpoong tofu")

    name = "Peanut satay ramen"
    source = "Wil Yeung"
    type_ = "dinner"
    url = "https://www.youtube.com/watch?v=fM3YG7jE_Ys"

    session.add(meal)
    session.commit()

    response = client.patch(
        f"/meals/{meal.id}",
        json={
            "name": name,
            "source": source,
            "type": type_,
            "url": url,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": meal.id,
        "name": name,
        "source": source,
        "type": type_,
        "url": url,
        "ingredients": [],
    }

    assert meal.name == name
    assert meal.source == source
    assert meal.type == type_
    assert meal.url == url


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
        "source": None,
        "type": None,
        "url": None,
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
