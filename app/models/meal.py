from sqlmodel import Field, SQLModel, Relationship
from app.models.meal_ingredient_link import MealIngredientLink


class Meal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str = Field(sa_column_kwargs={"unique": True})

    ingredients: list["Ingredient"] = Relationship(  # noqa: F821
        back_populates="meals", link_model=MealIngredientLink
    )
