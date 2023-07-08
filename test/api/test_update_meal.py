from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models.meal import Meal


def test_update_meal_name(session: Session, client: TestClient):
    old_meal_name = "Peanut satay ramen"
    new_meal_name = "Kkanpoong tofu"

    meal = Meal(name=old_meal_name)

    session.add(meal)
    session.commit()

    response = client.patch(
        f"/meals/{meal.id}",
        json={
            "name": new_meal_name,
        },
    )

    assert response.status_code == 204

    session.refresh(meal)
    assert meal.name == new_meal_name
