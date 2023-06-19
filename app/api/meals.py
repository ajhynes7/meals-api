from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel.sql.expression import select

from app.api.util import get_session
from app.models.meal import Meal

router = APIRouter()


@router.get("/meals")
def get_meals(session: Session = Depends(get_session)):

    statement = select(Meal)
    meals = session.exec(statement).all()

    return meals
