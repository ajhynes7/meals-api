import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from sqlmodel.sql.expression import select

from app.models.nutrient import Nutrient


@pytest.mark.parametrize("name", ["Peanut butter", "Toast"])
def test_add_nutrient(session: Session, client: TestClient, name: str):
    response = client.post("/nutrients", json={"name": name})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": name}

    statement = select(Nutrient)
    nutrient = session.execute(statement).scalar_one()

    assert nutrient.name == name
