
from m2s.service.simple_server import create_app
from m2s.predictors.sklearn_predictor import SklearnLinearPredictor

from model import MyLinearModel

model_path = 'my_model.pkl'
predictor = SklearnLinearPredictor.load(MyLinearModel, model_path)

# create service app
service_app = create_app(
            title='My Linear Model Service',
            predictor=predictor)