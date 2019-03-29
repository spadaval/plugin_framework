#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Image(ABC):
    @abstractmethod
    def __init__(self, data_manager, **params):
        self.data = None
        self.data_manager = data_manager
        self.params = params

    @abstractmethod
    def get_definition(self):
        pass

    @abstractmethod
    def handle_update(self, tile_key, data):
        pass

    @abstractmethod
    def scan(self):
        """
        Update the image. Typically called by the DataManager or TaskRunner.
        """
        pass
