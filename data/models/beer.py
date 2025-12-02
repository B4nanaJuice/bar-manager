from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from data.models.drink import Drink
from data.models.enums import BeerType

class Beer(Drink):
    __tablename__ = 'beer'

    id: Mapped[int] = mapped_column(ForeignKey('drink.id'), primary_key = True)
    type: Mapped[BeerType]
    degree: Mapped[float]

    __mapper_args__ = {
        'polymorphic_identity': 'beer'
    }

    def __repr__(self):
        return f'<Beer {self.name}>'