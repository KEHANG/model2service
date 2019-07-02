

class Predictor(object):
    """
    a ``Predictor`` is a thin wrapper around any model that handles JSON -> JSON predictions
    that can be used for serving models through the web API or making predictions in bulk.
    """
    def __init__(self, model):
        self._model = model

    def predict_json(self, input_json):
        instance = self._json_to_instance(input_json)
        return self.predict_instance(instance)

    def _json_to_instance(self, input_json):
        """
        Converts a JSON into an instance which the ``Predictor`` should pass through,
        such as tokenised inputs.
        """
        raise NotImplementedError

    def predict_instance(self, instance):
        outputs = self._model.forward_on_instance(instance)
        return outputs