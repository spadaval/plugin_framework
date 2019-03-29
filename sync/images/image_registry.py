image_classes = {}


def image_class(name):
    def wrapper(cls):
        image_classes[name] = cls
        return cls
