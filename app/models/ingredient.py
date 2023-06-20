from sqlmodel import Field, SQLModel


class Ingredient(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str
