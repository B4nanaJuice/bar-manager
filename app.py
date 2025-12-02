from flask import Flask

from data.database import init_database
from logger import configure_logging
from dotenv import load_dotenv
import os

from routes import public, auth, admin

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')

init_database(app = app)
configure_logging(app = app)

app.register_blueprint(public.page)
app.register_blueprint(auth.page)
app.register_blueprint(admin.page)

@app.errorhandler(404)
def page_not_found(error):
    return "404 - Page introuvable"