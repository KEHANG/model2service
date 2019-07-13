
import joblib
from sklearn.linear_model import LinearRegression

class MyLinearModel(LinearRegression):

    @classmethod
    def load(cls, model_path):

        model = joblib.load(model_path)
        return model

    def forward_on_instance(self, instance):

        return self.predict([instance])