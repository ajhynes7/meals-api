from sqlmodel import Field, Relationship, SQLModel

from app.models.ingredient import Ingredient
from app.models.meal_ingredient_link import MealIngredientLink


class MealBase(SQLModel):
    name: str = Field(sa_column_kwargs={"unique": True})

    source: str | None = None
    type: str | None = None
    url: str | None = None


class Meal(MealBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    ingredients: list[Ingredient] = Relationship(
        back_populates="meals", link_model=MealIngredientLink
    )


class MealRead(MealBase):
    id: int


class MealReadWithIngredients(MealRead):
    ingredients: list[Ingredient] = []


class MealUpdate(SQLModel):
    name: str | None = None

    source: str | None = None
    type: str | None = None
    url: str | None = None

    ingredient_names: list[str] | None = None
