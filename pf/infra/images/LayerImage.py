#!/usr/bin/python
# -*- coding: utf-8 -*-

from .Image import Image

from .image_registry import image_class

from .utils import grabImage, get_image_to_numpy


@image_class
class LayerImage(Image):
    def __init__(self, data_manager, mode, **kwargs):
        self.data = None
        self.data_manager = data_manager
        self.krita = mode == "client"
        if self.krita:
            self.layer_name = kwargs["layer"]
            self.layer = self.get_layer_from_name(self.layer_name)

    def get_dict(self):
        return {"layer": self.layer_name}

    def update_tile_data(self, data, tile_key=0):
        self.data_manager.update_tile(self, tile_key, data)

    def recv_tile_data(self, tile_key, data):
        # Handle data leaded from the server, write to krita
        self.data = data
        if self.krita:
            self.update_krita(tile_key, data)

    def update_krita(self, tile_key, data):
        pass

    def update(self):
        if self.mode == "client":
            imageData = grabImage(self.layer, 0, 0, 150, 150)
            image_numpy_format = get_image_to_numpy(imageData)
            self.update_data(image_numpy_format)
