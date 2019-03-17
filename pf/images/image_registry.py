image_classes = {}


def image_class(cls):
    image_classes[cls.__name__] = cls
    return cls
