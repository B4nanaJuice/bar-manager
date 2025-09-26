from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from data.database import db
from data.models.cocktail import Cocktail

class CocktailIngredient(db.Model):
    __tablename__ = 'cocktail_ingredients'

    id: Mapped[int] = mapped_column(unique = True, primary_key = True, autoincrement = True)
    cocktail_id: Mapped[int] = mapped_column(ForeignKey('cocktails.id'))
    name: Mapped[str]
    quantity: Mapped[float]
    cocktail: Mapped["Cocktail"] = relationship(back_populates = 'ingredients')
    