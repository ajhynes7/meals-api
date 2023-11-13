import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.ingredient import Ingredient
from app.models.nutrient import Nutrient


@pytest.mark.parametrize("name", ["Red lentils", "Black beans"])
def test_get_ingredient(session: Session, client: TestClient, name: str):
    ingredient = Ingredient(name=name)
    session.add(ingredient)

    response = client.get("/ingredients/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": name}


def test_get_ingredients(session: Session, client: TestClient):
    names = ["Red lentils", "Rice", "Garlic"]

    for name in names:
        ingredient = Ingredient(name=name)
        session.add(ingredient)

    response = client.get("/ingredients")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": names[0]},
        {"id": 2, "name": names[1]},
        {"id": 3, "name": names[2]},
    ]


def test_get_ingredients_by_nutrient(session: Session, client: TestClient):
    nutrient = Nutrient(name="Vitamin C")

    ingredients = [
        Ingredient(name=name) for name in ["Orange", "Grapefruit", "Cashews"]
    ]

    ingredients[0].nutrients.append(nutrient)
    ingredients[1].nutrients.append(nutrient)

    session.add_all(ingredients)
    session.commit()

    response = client.get("/ingredients", params={"nutrients": ["Vitamin C"]})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Orange"},
        {"id": 2, "name": "Grapefruit"},
    ]


def test_get_ingredients_by_multiple_nutrients(session: Session, client: TestClient):
    nutrients = [Nutrient(name=name) for name in ["Vitamin A", "Vitamin C"]]
    ingredients = [Ingredient(name=name) for name in ["Grapefruit", "Clementine"]]

    ingredients[0].nutrients.append(nutrients[0])
    ingredients[0].nutrients.append(nutrients[1])
    ingredients[1].nutrients.append(nutrients[1])

    session.add_all(ingredients)
    session.commit()

    response = client.get(
        "/ingredients", params={"nutrients": ["Vitamin A", "Vitamin C"]}
    )

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Grapefruit"},
    ]
