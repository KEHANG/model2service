import json
from flask import Flask, jsonify, request, Response

def create_app(title,
               predictor):
    """
    Creates a Flask app that serves up the provided ``Predictor``
    """

    app = Flask(__name__)

    @app.route('/')
    def index():
        return Response(response=title, status=200)

    @app.route('/predict', methods=['POST'])
    def predict():
        """make a prediction using the specified model and return the results"""
        data = request.get_json()

        prediction = predictor.predict_json(data)

        log_blob = {"inputs": data, "outputs": prediction}
        print(log_blob)

        return jsonify(prediction)

    return app

