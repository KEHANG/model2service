import json
from flask import abort, current_app, request, jsonify, Blueprint

bp = Blueprint('api', __name__)

@bp.route('/predict', methods=['POST'])
def predict():
    """make a prediction using the specified model and return the results"""
    data = request.get_json()

    prediction = current_app.predictor.predict_json(data)

    log_blob = {"inputs": data, "outputs": prediction}
    current_app.logger.info("prediction: %s", json.dumps(log_blob))

    return jsonify(prediction)