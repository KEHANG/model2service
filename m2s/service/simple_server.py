import os
import logging
from flask import Flask
from logging.handlers import RotatingFileHandler

def create_app(title,
               predictor,
               config=None):
    """
    Creates a Flask app that serves up the provided ``Predictor``
    """

    app = Flask(__name__)
    app.config.from_object(config)
    app.title = title
    app.predictor = predictor

    # register blueprints
    from m2s.service.blueprints.main import bp as main_bp
    from m2s.service.blueprints.api import bp as api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug and not app.testing:

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(f'logs/{app.title}.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info(f'{app.title} startup')

    return app

