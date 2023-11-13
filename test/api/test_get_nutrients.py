import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.nutrient import Nutrient


@pytest.mark.parametrize("name", ["Vitamin A", "Vitamin C"])
def test_get_nutrient(session: Session, client: TestClient, name: str):
    nutrient = Nutrient(name=name)
    session.add(nutrient)

    response = client.get("/nutrients/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": name}


def test_get_nutrients(session: Session, client: TestClient):
    names = ["Vitamin A", "Vitamin C", "Vitamin D"]

    for name in names:
        nutrient = Nutrient(name=name)
        session.add(nutrient)

    response = client.get("/nutrients")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": names[0]},
        {"id": 2, "name": names[1]},
        {"id": 3, "name": names[2]},
    ]
