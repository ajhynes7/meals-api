from sqlmodel import Field, SQLModel


class NutrientBase(SQLModel):
    name: str


class Nutrient(NutrientBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class NutrientRead(NutrientBase):
    id: int
