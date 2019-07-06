from PIL import Image
from overrides import overrides
import torchvision.transforms as T

from m2s.predictors.predictor import Predictor

class ObjectDetectionPredictor(Predictor):
    """
    Predictor for object detection in images.
    """

    @overrides
    def _json_to_instance(self, input_json):
        """
        Expects JSON that looks like ``{"image_path": "..."}``.
        """
        image_path = input_json["image_path"]
        # define image transforms
        transforms = T.Compose([T.ToTensor()])
        img = Image.open(image_path).convert("RGB")
        img_instance = transforms(img)
        return img_instance

    @classmethod
    def load(predictor_cls, model_cls, num_classes, weight_path):
        model = model_cls.load(num_classes, weight_path)
        predictor = predictor_cls(model)
        return predictor
