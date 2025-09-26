from flask import Flask

from routes import public, admin
from data.database import init_database

app = Flask(__name__)
init_database(app = app)

app.register_blueprint(public.page)
app.register_blueprint(admin.page)