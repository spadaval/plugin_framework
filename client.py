from pf.infra.data_manager import DataManager

import asyncio
import websockets
import logging

logger = logging.getLogger()


async def run_client():
    ws = await websockets.connect("ws://localhost:8765")
    data_manager = DataManager(ws, mode="client")
    logger.debug("Client init complete")
    await asyncio.gather(data_manager.channel.listen(), data_manager.watch_krita())


if __name__ == "__main__":
    asyncio.run(run_client(), debug=True)
