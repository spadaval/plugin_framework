from pf.infra.data_manager import DataManager

import asyncio
import websockets
import logging

logger = logging.getLogger()

data_manager = None


async def handle_message(ws, path):
    logger.debug("Running handler...")
    global data_manager
    if data_manager is None:
        data_manager = DataManager(ws, mode="server")
        logger.debug("Server init complete")

    logger.debug("Waiting for message...")
    message = await ws.recv()
    logger.debug("Got message!")
    data_manager.channel.process_message(message)


def run_server():
    start_server = websockets.serve(handle_message, "localhost", 8765)
    logger.debug("Starting server...")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    run_server()
