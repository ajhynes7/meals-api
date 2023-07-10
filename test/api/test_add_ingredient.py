import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from sqlmodel.sql.expression import select

from app.models.ingredient import Ingredient


@pytest.mark.parametrize("name", ["Peanut butter", "Toast"])
def test_add_ingredient(session: Session, client: TestClient, name: str):
    response = client.post("/ingredients", json={"name": name})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": name}

    statement = select(Ingredient)
    ingredient = session.execute(statement).scalar_one()

    assert ingredient.name == name
