import logging
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    app.logger.setLevel(logging.INFO)
    file_handler = RotatingFileHandler('logs/flask_app.log', maxBytes = 1024 * 1024 * 10, backupCount = 5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    if not app.logger.handlers:
        app.logger.addHandler(file_handler)
    file_handler.setLevel(logging.INFO)