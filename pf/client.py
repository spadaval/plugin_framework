from pf.infra.data_manager import DataManager

import asyncio
import websockets
import logging

logger = logging.getLogger()


async def start():
    ws = await websockets.connect("ws://localhost:8765")
    data_manager = DataManager(ws, mode="client")
    logger.debug("Client init complete")
    await asyncio.gather(data_manager.channel.listen(), data_manager.watch_krita())


def run_client():
    asyncio.get_event_loop().run_until_complete(start())
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    run_client()
