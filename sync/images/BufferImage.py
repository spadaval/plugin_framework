#!/usr/bin/python
# -*- coding: utf-8 -*-

from .images.Image import Image
from .image_registry import image_class


@image_class("buffer")
class BufferImage(Image):
    def __init__(self):
        self.data = None
