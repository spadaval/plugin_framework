#!/usr/bin/python
# -*- coding: utf-8 -*-

from .Image import Image

from .image_registry import image_class


@image_class
class ComputedImage(Image):
    def __init__(self, data_manager, mode, **kwargs):
        self.data = None
        self.data_manager = data_manager

    def get_dict(self):
        return {"layer": self.layer_name}

    def update_tile_data(self, tile_key, data):
        self.data_manager.update_tile_data()

    def update_data(self, data):
        self.data_manager.update_tile_data()

    def recv_tile_data(self, tile_key, data):
        if self.mode == "client":
            self.update_krita(tile_key, data)

    def update(self):
        if self.mode == "client":
            return
