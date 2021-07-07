#!/usr/bin/env python

# WS server example

import asyncio
import json

import websockets

from mipi.base_codemeaning_predictor import PatchInfo
from mipi.mipi_app import Mipi

port = 8765
address = "localhost"

mipi = Mipi()


async def evaluate_patch(websocket, patch_info):
    print('Begin evaluate patch')
    patch = PatchInfo()
    patch.from_json(patch_info)
    result = mipi.evaluate(patch)
    print('End evaluate patch, results: \n%s' % result)
    message = result.to_json()
    print('Begin send message: %s' % message)
    await websocket.send(message)


async def hello(websocket, path):
    # await register(websocket)
    print("hello begin, path: %s, ws: %s" % (path, websocket))
    # data = await websocket.recv()
    async for message in websocket:
        print("message: %s" % message)
        try:
            patch_info = json.loads(message)
            await evaluate_patch(websocket, patch_info)
        except ValueError as e:
            response_msg = "NOT JSON: %s" % message
            print("response message: %s" % response_msg)
            # await asyncio.wait(websocket.send(response_msg))
            await websocket.send(response_msg)
    print("hello end, path: %s, ws: %s" % (path, websocket))

print("Beginning")
start_server = websockets.serve(hello, address, port)
print("Init")
asyncio.get_event_loop().run_until_complete(start_server)
print("started")
asyncio.get_event_loop().run_forever()
print("stopped")


# async def evaluate_patch(websocket, patch_info):
#     patch_id = patch_info["PatchId"];
#     bug_id = patch_info["BugId"];
#     method_names = []
#     for triple in patch_info["PatchedMethods"]:
#         method_names.append(triple["DevIntention"])
#     response_msg = 'Patch: %s, Bug: %s, Methods: %s' % (patch_id, bug_id, method_names)
#     print("response message: %s" % response_msg)
#     await websocket.send(response_msg)
