import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models.ingredient import Ingredient


@pytest.mark.parametrize("name", ["Red lentils", "Black beans"])
def test_read_ingredient(session: Session, client: TestClient, name: str):
    ingredient = Ingredient(name=name)
    session.add(ingredient)

    response = client.get("/ingredients/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": name}


def test_read_ingredients(session: Session, client: TestClient):
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
