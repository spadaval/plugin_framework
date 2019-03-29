import bson
import logging

logger = logging.getLogger(__name__)


class Channel:
    def __init__(self, ws, data_manager):
        self.ws = ws
        self.data_manager = data_manager

    async def send_message(self, request, data):
        message = {"request": request, "data": data}
        self.ws.send(bson.dumps(message))

    async def process_message(self, message):
        r = bson.load(message)
        logger.debug("Got message {}".format(r))
        request = r['request']
        data = r["data"]
        if request == "RegisterImage":
            self.data_manager.recv_image_definition(**data)
        elif request == "UpdateTileData":
            self.data_manager.recv_tile_update(**data)
        # elif message["request"] == "RegisterImage":
        #    self.data_manager.update_tile()

    async def listen(self):
        logger.debug("Listening for updates...")
        while True:
            message = await self.ws.recv()
            logger.debug("Got a message!")
            await self.process_message(message)
