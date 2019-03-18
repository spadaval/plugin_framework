#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import logging
import random

from .channel import Channel
from .utils import load_image
from .images import LayerImage, ComputedImage

logger = logging.getLogger(__name__)


class DataManager:
    def __init__(self, ws, mode="client"):
        self.layer_images = {}
        self.computed_images = {}
        self.dependencies = {}
        self.reverse = {}
        self.channel = Channel(ws, self)
        self.mode = mode

    def get_new_uuid(self):
        n = random.randrange(10000)
        while n in self.images:
            n = random.randrange(10000)
        logger.debug("Issued id {} for new image".format(n))
        return n

    def register_image(self, image, uuid=None):
        if uuid is None:
            uuid = self.get_new_uuid()
        logger.debug("Registering new image with uuid {}".format(uuid))
        obj = {
            "class": image.__name__,
            "object": image,
            "tile_map": image.get_tile_dict(),
        }
        if isinstance(image, LayerImage):
            self.layer_images[uuid] = obj
        elif isinstance(image, ComputedImage):
            self.computed_images[uuid] = obj
        else:
            logger.error("Unknown image type")
        self.reverse[image] = uuid
        return uuid

    async def update_tile(self, image, key, tile_data):
        uuid = self.reverse[image]
        logger.debug("Handling local tile {} update in image {}...".format(key, uuid))
        message_data = {"uuid": uuid, "tile_key": key, "data": tile_data}

        await self.channel.send_message("UpdateTileData", message_data)
        for dependent in self.dependencies[image]:
            dependent.update()

    async def recv_tile_update(self, uuid, key, tile_data):
        logger.debug("Updating tile {} in image {}".format(key, uuid))
        image = self.reverse[uuid]
        image.update_tile_data(key, tile_data)

    async def send_image_definition(self, image):
        image_dict = image.get_dict()
        image_dict["uuid"] = self.reverse[image]
        logger.debug("Updating remote about new image {}...".format(image_dict))
        await self.channel.send_message("RegisterImage", image_dict)

    async def recv_image_definition(self, image_dict):
        logger.debug("Loading remote image...")
        if image_dict["uuid"] in self.images:
            logger.warn("Image already exists (or uuid collision)...")
            return

        image_dict["mode"] = self.mode  # inject the mode of operation
        image_dict["data_manager"] = self  # inject the data manager
        image = load_image(image_dict)
        self.register_image(image, uuid=image_dict["uuid"])
        logger.debug("Remote image loaded successfully")

    def add_dependency(self, source, dependent):
        if source not in self.dependencies:
            self.dependencies[source] = []

        self.dependencies[source].append(dependent)

    async def watch_krita(self):
        while True:
            logger.debug("Scanning layer images...")
            for uuid, image in self.layer_images:
                if image.update():
                    for dependent in self.dependencies[image]:
                        image.update()

            await asyncio.sleep(2)
