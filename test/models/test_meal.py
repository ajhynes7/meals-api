from sqlmodel import Session

from app.models.meal import Meal


def test_meal(session: Session):
    meal = Meal(name="Hummus")

    assert meal.id is None

    session.add(meal)
    session.commit()

    assert meal.id == 1
    assert meal.name == "Hummus"
