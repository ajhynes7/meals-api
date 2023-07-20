import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from sqlmodel.sql.expression import select

from app.models.meal import Meal


@pytest.mark.parametrize("name", ["Peanut satay ramen", "Kkanpoong tofu"])
def test_add_meal(session: Session, client: TestClient, name: str):
    name = "Peanut satay ramen"
    source = "Wil Yeung"
    type_ = "dinner"
    url = "https://www.youtube.com/watch?v=fM3YG7jE_Ys"

    response = client.post(
        "/meals",
        json={
            "name": name,
            "source": source,
            "type": type_,
            "url": url,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": name,
        "source": source,
        "type": type_,
        "url": url,
    }

    statement = select(Meal)
    meal = session.execute(statement).scalar_one()

    assert meal.name == name
    assert meal.source == source
    assert meal.type == type_
    assert meal.url == url


@pytest.mark.parametrize("name", ["Peanut satay ramen", "Kkanpoong tofu"])
def test_add_meal_with_duplicate_name(session: Session, client: TestClient, name: str):
    response = client.post("/meals", json={"name": name})
    assert response.status_code == 201

    response = client.post("/meals", json={"name": name})
    assert response.status_code == 409
    assert response.json() == {"detail": "This name already exists."}
