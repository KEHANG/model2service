import joblib
from model import MyLinearModel

model = MyLinearModel()

model.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])

joblib.dump(model, 'pretrained/my_model.pkl')