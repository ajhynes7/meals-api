from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.ingredient import Ingredient
from app.models.meal import Meal


def test_read_meal(session: Session, client: TestClient):
    name = "Red lentil curry"
    meal = Meal(name=name)

    session.add(meal)
    session.commit()

    response = client.get("/meals/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": name, "ingredients": []}


def test_read_nonexistent_meal(session: Session, client: TestClient):
    response = client.get("/meals/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "This meal does not exist."}


def test_read_meal_with_ingredients(session: Session, client: TestClient):
    meal_name = "Red lentil curry"
    ingredient_names = ["Red lentils", "Curry powder"]

    meal = Meal(name=meal_name)
    ingredients = [Ingredient(name=name) for name in ingredient_names]

    meal.ingredients = ingredients

    session.add(meal)
    session.commit()

    response = client.get("/meals/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": meal_name,
        "ingredients": [
            {"id": 1, "name": ingredient_names[0]},
            {"id": 2, "name": ingredient_names[1]},
        ],
    }


def test_read_meals(session: Session, client: TestClient):
    names = ["Red lentil curry", "Miso broth ramen", "Kale lentil potato bowl"]

    for name in names:
        meal = Meal(name=name)
        session.add(meal)

    response = client.get("/meals")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": names[0]},
        {"id": 2, "name": names[1]},
        {"id": 3, "name": names[2]},
    ]


def test_read_meals_by_ingredient(session: Session, client: TestClient):
    ingredient = Ingredient(name="Chickpeas")

    meals = [Meal(name=name) for name in ["Hummus", "Falafel", "PB&J"]]

    meals[0].ingredients.append(ingredient)
    meals[1].ingredients.append(ingredient)

    session.add_all(meals)
    session.commit()

    response = client.get("/meals", params={"ingredients": ["Chickpeas"]})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Hummus"},
        {"id": 2, "name": "Falafel"},
    ]


def test_read_meals_by_multiple_ingredients(session: Session, client: TestClient):
    ingredients = [Ingredient(name=name) for name in ["Chickpeas", "Garlic"]]
    meals = [Meal(name=name) for name in ["Hummus", "Falafel", "PB&J"]]

    meals[0].ingredients.append(ingredients[0])
    meals[0].ingredients.append(ingredients[1])
    meals[1].ingredients.append(ingredients[0])

    session.add_all(meals)
    session.commit()

    response = client.get("/meals", params={"ingredients": ["Chickpeas", "Garlic"]})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Hummus"},
    ]
