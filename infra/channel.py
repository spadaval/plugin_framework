import bson
import logging

logger = logging.getLogger(__name__)


class Channel:
    def __init__(self, ws, data_manager):
        self.ws = ws
        self.data_manager = data_manager

    async def send_message(self, request, message):
        message = {"request": request, "data": message}
        self.ws.send(bson.dumps(message))

    async def process_message(self, message):
        if message["request"] == "":
            self.data_manager.update_tile()

    async def run_loop(self):
        logger.debug("Begin loop...")
        while True:
            message = await self.ws.recv()
            await self.process_message(message)
