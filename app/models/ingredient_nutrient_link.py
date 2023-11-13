from sqlmodel import Field, SQLModel


class IngredientNutrientLink(SQLModel, table=True):
    __tablename__ = "ingredient_nutrient"

    ingredient_id: int = Field(foreign_key="ingredient.id", primary_key=True)
    nutrient_id: int = Field(foreign_key="nutrient.id", primary_key=True)


class IngredientNutrientLinkbyName(SQLModel):
    ingredient_name: str
    nutrient_name: str
