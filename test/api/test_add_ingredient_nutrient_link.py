from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.ingredient import Ingredient
from app.models.nutrient import Nutrient


def test_add_ingredient_nutrient_link(session: Session, client: TestClient):
    ingredient_name = "Orange"
    nutrient_name = "Vitamin C"

    ingredient = Ingredient(name=ingredient_name)
    nutrient = Nutrient(name=nutrient_name)

    session.add(ingredient)
    session.add(nutrient)
    session.commit()

    response = client.post(
        "/ingredient-nutrient",
        json={"ingredient_id": ingredient.id, "nutrient_id": nutrient.id},
    )

    assert response.status_code == 201
    assert response.json() == {
        "ingredient_id": ingredient.id,
        "nutrient_id": nutrient.id,
    }

    session.refresh(ingredient)
    session.refresh(nutrient)

    assert ingredient.nutrients == [nutrient]
    assert nutrient.ingredients == [ingredient]
