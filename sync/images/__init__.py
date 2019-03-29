from .image_registry import image_classes
from .ComputedImage import ComputedImage
from .LayerImage import LayerImage


def load_image_definition(image_dict, data_manager):
    cls = image_classes[image_dict["type"]]
    return cls(**image_dict, data_manager=data_manager)


__all__ = ["image_classes", "ComputedImage", "LayerImage"]
