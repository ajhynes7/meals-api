from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.api.util import get_session
from app.models.nutrient import Nutrient

router = APIRouter()


@router.get("/nutrients/{nutrient_id}")
def get_nutrient(nutrient_id: int, session: Session = Depends(get_session)) -> Nutrient:
    return session.get(Nutrient, nutrient_id)


@router.get("/nutrients")
def get_nutrients(session: Session = Depends(get_session)) -> list[Nutrient]:
    statement = select(Nutrient).order_by(Nutrient.id)
    return session.exec(statement).all()


@router.post("/nutrients", status_code=201)
def add_nutrient(
    nutrient: Nutrient, session: Session = Depends(get_session)
) -> Nutrient:
    session.add(nutrient)

    session.commit()
    session.refresh(nutrient)

    return nutrient
