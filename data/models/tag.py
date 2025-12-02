from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from data.database import db
from data.models.enums import TagName

class Tag(db.Model):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(unique = True, primary_key = True, autoincrement = True)
    name: Mapped[TagName]
    drink_id: Mapped[int] = mapped_column(ForeignKey('drink.id'))

    def __repr__(self):
        return f'<Tag {self.name}>'