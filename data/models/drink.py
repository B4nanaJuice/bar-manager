from sqlalchemy.orm import Mapped, mapped_column, relationship
from data.database import db
from data.models.tag import Tag
from typing import List

class Drink(db.Model):
    __tablename__ = 'drink'

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str]
    is_available: Mapped[bool] = mapped_column(default = True)
    tags: Mapped[List['Tag']] = relationship(
        cascade = 'all, delete-orphan'
    )
    drink_type: Mapped[str]

    __mapper_args__ = {
        'polymorphic_on': 'drink_type',
        'polymorphic_identity': 'drink'
    }

    def __repr__(self):
        return f'<Drink {self.name}>'