from sqlmodel import Field, Relationship, SQLModel

from app.models.ingredient import Ingredient
from app.models.ingredient_nutrient_link import IngredientNutrientLink


class NutrientBase(SQLModel):
    name: str


class Nutrient(NutrientBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    ingredients: list[Ingredient] = Relationship(
        back_populates="nutrients", link_model=IngredientNutrientLink
    )


class NutrientRead(NutrientBase):
    id: int
