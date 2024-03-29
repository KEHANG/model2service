from overrides import overrides
from m2s.predictors.predictor import Predictor

class SklearnLinearPredictor(Predictor):
    """
    a ``SklearnLinearPredictor`` predicts output
    using a linear model.
    """
    @overrides
    def _json_to_instance(self, input_json):
        """
        Expects JSON that looks like
        ``{"x": list[float]}``.
        """
        if  "x" not in input_json:
            raise AssertionError("Expect x to be in the input, but not there.")
        instance = input_json["x"]
        return instance

    @classmethod
    def load(predictor_cls, model_cls, model_path):
        model = model_cls.load(model_path)
        predictor = predictor_cls(model)
        return predictor