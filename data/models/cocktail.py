from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from data.models.drink import Drink
from data.models.enums import CocktailType, Glass, MixMethod
from data.models.cocktail_ingredient import CocktailIngredient
from typing import List

class Cocktail(Drink):
    __tablename__ = 'cocktail'

    id: Mapped[int] = mapped_column(ForeignKey('drink.id'), primary_key = True)
    type: Mapped[CocktailType]
    has_alcohol: Mapped[bool]
    glass: Mapped[Glass]
    mix_method: Mapped[MixMethod]
    garnish: Mapped[str] = mapped_column(nullable = True)
    ingredients: Mapped[List["CocktailIngredient"]] = relationship(
        cascade = 'all, delete-orphan'
    )

    __mapper_args__ = {
        'polymorphic_identity': 'cocktail'
    }

    def __repr__(self):
        return f'<Cocktail {self.name}>'