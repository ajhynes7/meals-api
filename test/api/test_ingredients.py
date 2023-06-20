import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models.ingredient import Ingredient


@pytest.mark.parametrize("name", ["Red lentils", "Black beans"])
def test_get_ingredient(session: Session, client: TestClient, name: str):
    ingredient = Ingredient(name=name)
    session.add(ingredient)

    response = client.get("/ingredients")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": name},
    ]
