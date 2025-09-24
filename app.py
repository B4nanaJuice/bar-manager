from flask import Flask

from routes import public, admin

app = Flask(__name__)

app.register_blueprint(public.page)
app.register_blueprint(admin.page)