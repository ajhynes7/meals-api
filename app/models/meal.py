from sqlmodel import Field, SQLModel, Relationship
from app.models.meal_ingredient_link import MealIngredientLink
from app.models.ingredient import Ingredient


class MealBase(SQLModel):
    name: str = Field(sa_column_kwargs={"unique": True})


class Meal(MealBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    ingredients: list[Ingredient] = Relationship(  # noqa: F821
        back_populates="meals", link_model=MealIngredientLink
    )


class MealRead(MealBase):
    id: int


class MealReadWithIngredients(MealRead):
    ingredients: list[Ingredient] = []


class MealUpdate(SQLModel):
    name: str | None = None

    ingredient_ids: list[int] | None = None
