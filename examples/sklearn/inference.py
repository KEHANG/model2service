
from m2s.predictors.sklearn_predictor import SklearnLinearPredictor

from model import MyLinearModel

model_path = 'my_model.pkl'
predictor = SklearnLinearPredictor.load(MyLinearModel, model_path)

input_json = {"x": [1, 4]}
prediction = predictor.predict_json(input_json)
print(prediction)