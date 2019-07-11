import six
import torch
import numpy

def sanitize(x):
    """
    Sanitize turns PyTorch and Numpy types into basic Python types so they
    can be serialized into JSON.
    """
    if six.PY3 and isinstance(x, (str, float, int, bool)):
        # x is already serializable
        return x
    elif six.PY2 and isinstance(x, (str, unicode, float, int, bool)):
        return x
    elif isinstance(x, torch.Tensor):
        # tensor needs to be converted to a list (and moved to cpu if necessary)
        return x.cpu().tolist()
    elif isinstance(x, numpy.ndarray):
        # array needs to be converted to a list
        return x.tolist()
    elif isinstance(x, numpy.number):  # pylint: disable=no-member
        # NumPy numbers need to be converted to Python numbers
        return x.item()
    elif isinstance(x, dict):
        # Dicts need their values sanitized
        return {key: sanitize(value) for key, value in x.items()}
    elif isinstance(x, (list, tuple)):
        # Lists and Tuples need their values sanitized
        return [sanitize(x_i) for x_i in x]
    elif x is None:
        return "None"
    elif hasattr(x, 'to_json'):
        return x.to_json()
    else:
        raise ValueError("Cannot sanitize {0} of {1}.".format(x, type(x)) + 
                         "If this is your own custom class, add a `to_json(self)` method " + 
                         "that returns a JSON-like object.")