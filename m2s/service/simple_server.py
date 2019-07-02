import os
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request, Response

def create_app(title,
               predictor):
    """
    Creates a Flask app that serves up the provided ``Predictor``
    """

    app = Flask(__name__)

    if not app.debug and not app.testing:

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(f'logs/{title}.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info(f'{title} startup')

    @app.route('/')
    def index():
        return Response(response=title, status=200)

    @app.route('/predict', methods=['POST'])
    def predict():
        """make a prediction using the specified model and return the results"""
        data = request.get_json()

        prediction = predictor.predict_json(data)

        log_blob = {"inputs": data, "outputs": prediction}
        app.logger.info("prediction: %s", json.dumps(log_blob))

        return jsonify(prediction)

    return app

