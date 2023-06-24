from sqlmodel import Field, SQLModel, Relationship
from app.models.meal_ingredient_link import MealIngredientLink


class Ingredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    meals: list["Meal"] = Relationship(  # noqa: F821
        back_populates="ingredients", link_model=MealIngredientLink
    )
