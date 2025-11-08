from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from data.database import db

from data.models.cocktail import Cocktail
from data.models.beer_stock import BeerStock

class Order(db.Model):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(unique = True, primary_key = True, autoincrement = True)
    client: Mapped[str] = mapped_column(nullable = False)
    cocktail_id: Mapped[int] = mapped_column(ForeignKey('cocktails.id'))
    cocktail: Mapped["Cocktail"] = relationship()
    beer_id: Mapped[int] = mapped_column(ForeignKey('beer_stocks.id'))
    beer: Mapped["BeerStock"] = relationship()

    def __repr__(self):
        return f"<Order {self.id}>"