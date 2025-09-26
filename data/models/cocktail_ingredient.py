from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from data.database import db

class CocktailIngredient(db.Model):
    __tablename__ = 'cocktail_ingredients'

    id: Mapped[int] = mapped_column(unique = True, primary_key = True, autoincrement = True)
    cocktail_id: Mapped[int] = mapped_column(ForeignKey('cocktails.id'))
    name: Mapped[str]
    quantity: Mapped[float]

    def __repr__(self):
        return f"<CocktailIngredient {self.quantity}cl {self.name}>"