#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import random

from .channel import Channel
from .utils import load_image

logger = logging.getLogger(__name__)


class DataManager:
    def __init__(self, ws, mode="client"):
        self.images = {}
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

        self.images[uuid] = {
            "class": image.__name__,
            "object": image,
            "tile_map": image.get_tile_dict(),
        }
        self.reverse[image] = uuid
        return uuid

    async def update_tile(self, image, key, tile_data):
        uuid = self.reverse[image]
        logger.debug("Handling local tile {} update in image {}...".format(key, uuid))
        message_data = {"uuid": uuid, "tile_key": key, "data": tile_data}
        await self.channel.send_message("UpdateTileData", message_data)

    async def recv_tile_update(self, uuid, key, tile_data):
        logger.debug("Updating tile {} in image {}".format(key, uuid))
        image = self.reverse[uuid]
        image.update_tile_data(key, tile_data)

    async def send_image_definition(self, image):
        logger.debug("Updating remote about new image...")
        await self.channel.send_message("RegisterImage", image.get_dict())

    async def recv_image_definition(self, image_dict):
        logger.debug("Loading remote image...")
        image_dict["krita"] = self.mode == "client"  # inject the mode of operation
        image_dict["data_manager"] = self  # inject the data manager
        image = load_image(image_dict)
        self.register_image(image, uuid=image_dict["uuid"])

    async def handle_message(self, message):
        await self.channel.handle_message(message)
