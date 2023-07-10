from sqlmodel import Session

from app.models.ingredient import Ingredient


def test_ingredient(session: Session):
    ingredient = Ingredient(name="Chickpeas")

    assert ingredient.id is None

    session.add(ingredient)
    session.commit()

    assert ingredient.id == 1
    assert ingredient.name == "Chickpeas"
