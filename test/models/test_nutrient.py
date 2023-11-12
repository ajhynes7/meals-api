from sqlmodel import Session

from app.models.nutrient import Nutrient


def test_nutrient(session: Session):
    nutrient_name = "Vitamin A"
    nutrient = Nutrient(name=nutrient_name)

    assert nutrient.id is None

    session.add(nutrient)
    session.commit()

    assert nutrient.id == 1
    assert nutrient.name == nutrient_name
