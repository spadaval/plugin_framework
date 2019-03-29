#!/usr/bin/python
# -*- coding: utf-8 -*-

from .Image import Image

# from .image_registry import image_class

from .utils import grabImage, get_image_to_numpy


# @image_class("layer")
class LayerImage(Image):
    def __init__(self, data_manager, x0, y0, x, y, w, layer_name):
        self.data = None
        self.data_manager = data_manager

    def get_definition(self):
        return {
            "layer": self.layer_name,
            "x0": self.x0,
            "y0": self.y0,
            "x": self.x,
            "y": self.y,
            "w": self.w,
        }
