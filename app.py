from flask import Flask, render_template

from routes import public, admin, auth, api
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
app.register_blueprint(api.page)

# Add app error handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', page_title = "Page introuvable")