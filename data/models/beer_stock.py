from sqlalchemy.orm import Mapped, mapped_column
from data.database import db

class BeerStock(db.Model):
    __tablename__ = 'beer_stocks'

    id: Mapped[int] = mapped_column(unique = True, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(unique = True) 
    type: Mapped[str]
    degree: Mapped[float]

    def __repr__(self):
        return f"<BeerStock {self.name}>"