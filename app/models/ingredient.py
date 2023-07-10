from sqlmodel import Field, Relationship, SQLModel

from app.models.meal_ingredient_link import MealIngredientLink


class IngredientBase(SQLModel):
    name: str


class Ingredient(IngredientBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    meals: list["Meal"] = Relationship(  # noqa: F821
        back_populates="ingredients", link_model=MealIngredientLink
    )


class IngredientRead(IngredientBase):
    id: int
