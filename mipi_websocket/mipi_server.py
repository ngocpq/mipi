#!/usr/bin/env python

import asyncio
import json

import websockets

from mipi.base_codemeaning_predictor import PatchInfo
from mipi.mipi_app import Mipi


class MipiWSServer:
    def __init__(self, mipi_obj, address="localhost", port=8765, port_admin=8766):
        self.port = port
        self.port_admin = port_admin
        self.address = address
        self.mipi = mipi_obj

    async def shutdown(self):
        print('stopping ws server')
        asyncio.get_event_loop().stop()
        print('ws server stopped')

    async def evaluate_patch(self, websocket, patch_info):
        print('Begin evaluate patch')
        patch = PatchInfo()
        patch.from_json(patch_info)
        result = self.mipi.evaluate(patch)
        print('End evaluate patch, results: \n%s' % result)
        message = result.to_json()
        print('Begin send message: %s' % message)
        await websocket.send(message)

    async def hello(self, websocket, path):
        # await register(websocket)
        print("hello begin, path: %s, ws: %s" % (path, websocket))
        # data = await websocket.recv()
        async for message in websocket:
            print("message: %s" % message)
            try:
                patch_info = json.loads(message)
                await self.evaluate_patch(websocket, patch_info)
            except ValueError as e:
                response_msg = "NOT JSON: %s" % message
                print("response message: %s" % response_msg)
                # await asyncio.wait(websocket.send(response_msg))
                await websocket.send(response_msg)
        print("hello end, path: %s, ws: %s" % (path, websocket))

    async def shutdown_ws_server(self, websocket, path):
        print("shutdown begin: ws: %s, path: %s" % (websocket, path))
        await self.shutdown()

    def start(self):
        start_server = websockets.serve(self.hello, self.address, self.port)
        print("Starting")
        asyncio.get_event_loop().run_until_complete(start_server)
        print(f'Listening for requests at [ws://{self.address}:{self.port}]')

        shutdown_server = websockets.serve(self.shutdown_ws_server, self.address, self.port_admin)
        # print('start admin')
        asyncio.get_event_loop().run_until_complete(shutdown_server)

        asyncio.get_event_loop().run_forever()
        # print("stopped")


if __name__ == '__main__':
    mipi = Mipi()

    server = MipiWSServer(mipi)
    server.start()
