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
