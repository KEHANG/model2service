import os
import json
from werkzeug.utils import secure_filename
from flask import current_app, request, jsonify, Blueprint

bp = Blueprint('api', __name__)

@bp.route('/predict', methods=['POST'])
def predict():
    """make a prediction using the specified model and return the results"""
    data = request.get_json()

    prediction = current_app.predictor.predict_json(data)

    log_blob = {"inputs": data, "outputs": prediction}
    current_app.logger.info("prediction: %s", json.dumps(log_blob))

    return jsonify(prediction)

@bp.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and allowed_file(file.filename, 
                    current_app.config['ALLOWED_EXTENSIONS']):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return filename

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions