import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models.meal import Meal


@pytest.mark.parametrize("name", ["Peanut satay ramen", "Kkanpoong tofu"])
def test_get_meal(session: Session, client: TestClient, name: str):

    meal = Meal(name=name)
    session.add(meal)

    response = client.get("/meals")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": name},
    ]
