from .infra.data_manager import DataManager

import websockets
import logging
import os

logger = logging.getLogger()


def init_logger(level, path):
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(path)
    fh.setLevel(logging.DEBUG)
    # create console handler with a provided log level
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


path = os.path.join(os.getcwd(), "log.txt")
init_logger(logging.DEBUG, path)


async def run_client():
    ws = await websockets.connect("ws://localhost:8765")
    data_manager = DataManager(ws, mode="client")
    logger.debug("Client init complete")
    await data_manager.channel.run_loop()


async def run_server():
    ws = await websockets.serve("ws://localhost:8765")
    data_manager = DataManager(ws, mode="client")
    logger.debug("Client init complete")
    await data_manager.channel.run_loop()
