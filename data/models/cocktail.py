from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from data.database import db
from data.models.cocktail_ingredient import CocktailIngredient

class Cocktail(db.Model):
    __tablename__ = 'cocktails'

    id: Mapped[int] = mapped_column(unique = True, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(unique = True)
    type: Mapped[str]
    has_alcohol: Mapped[bool]
    ingredients: Mapped[List["CocktailIngredient"]] = relationship()

    def __repr__(self):
        return f"<Cocktail {self.name}>"