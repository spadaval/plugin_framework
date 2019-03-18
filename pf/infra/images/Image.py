#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Image(ABC):
    def __init__(self, data_manager, krita=True):
        self.data = None
        self.krita = krita
        self.data_manager = data_manager
        self.data_manager.register_image(self)

    @abstractmethod
    def get_dict(self):
        pass

    @abstractmethod
    def recv_tile_data(self, tile_key, data):
        pass

    @abstractmethod
    def update(self):
        """
        Update the image. Called periodically, or when dependencies change.
        Should return boolean, True -> change occurred.
        This allows the system to update its dependencies.
        """
        pass