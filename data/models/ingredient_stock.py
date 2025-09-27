from sqlalchemy.orm import Mapped, mapped_column
from data.database import db

class IngredientStock(db.Model):
    __tablename__ = 'ingredient_stocks'

    id: Mapped[int] = mapped_column(unique = True, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(unique = True)

    def __repr__(self):
        return f"<IngredientStock {self.name}>"