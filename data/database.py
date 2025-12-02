from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from os import getenv

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)

def init_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
    db.init_app(app)

    with app.app_context():
        db.create_all()