#!/usr/bin/python
# -*- coding: utf-8 -*-

from .Image import Image

# from .image_registry import image_class


# @image_class("computed")
class ComputedImage(Image):
    def __init__(self, data_manager, inputs, model_id):
        self.data_manager = data_manager
        self.inputs = inputs
        self.model_id = model_id

    def get_definition(self):
        return {"inputs": self.inputs, "model_id": self.model_id}
