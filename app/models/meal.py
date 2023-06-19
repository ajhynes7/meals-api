
from sqlmodel import Field, SQLModel


class Meal(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str
