from flask import Flask

from routes import public, admin, auth
from data.database import init_database
from dotenv import load_dotenv
import os

load_dotenv()

# App initialization
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
init_database(app = app)

# Add paths to app
app.register_blueprint(public.page)
app.register_blueprint(admin.page)
app.register_blueprint(auth.page)