from sqlmodel import Field, SQLModel


class MealIngredientLink(SQLModel, table=True):
    __tablename__ = "meal_ingredient"

    meal_id: int = Field(foreign_key="meal.id", primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredient.id", primary_key=True)
