import pytest
from sqlmodel.sql.expression import select
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models.meal import Meal


@pytest.mark.parametrize("name", ["Peanut satay ramen", "Kkanpoong tofu"])
def test_add_meal(session: Session, client: TestClient, name: str):
    response = client.post("/meals", json={"name": name})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": name}

    statement = select(Meal)
    meal = session.execute(statement).scalar_one()

    assert meal.name == name
