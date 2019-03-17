#!/usr/bin/python
# -*- coding: utf-8 -*-

from .images.Image import Image

from .image_registry import image_class


@image_class
class ComputedImage(Image):
    pass
