from ..images import image_classes


def load_image(image_dict, data_manager):
    cls = image_classes[image_dict["class"]]
    return cls(**image_dict, data_manager=data_manager)
