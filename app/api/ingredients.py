from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel.sql.expression import select

from app.api.util import get_session
from app.models.ingredient import Ingredient

router = APIRouter()


@router.get("/ingredients")
def get_ingredients(session: Session = Depends(get_session)):
    statement = select(Ingredient)
    ingredients = session.exec(statement).all()

    return ingredients


@router.post("/ingredients", status_code=201)
def add_ingredient(ingredient: Ingredient, session: Session = Depends(get_session)):
    session.add(ingredient)

    session.commit()
    session.refresh(ingredient)

    return ingredient
