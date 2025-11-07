from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from data.database import db

class Order(db.Model):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(unique = True, primary_key = True, autoincrement = True)
    client: Mapped[str] = mapped_column(nullable = False)
    cocktail: Mapped[int] = mapped_column(ForeignKey('cocktails.id'), nullable = True)
    beer: Mapped[int] = mapped_column(ForeignKey('beer_stocks.id'), nullable = True)

    def __repr__(self):
        return f"<Order {self.id}>"