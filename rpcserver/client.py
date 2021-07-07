#!/usr/bin/env python

# WS client example

import asyncio
import json

import websockets


async def hello():
    uri = "ws://localhost:8765/xyz"
    async with websockets.connect(uri) as websocket:
        msg = json.dumps({'PatchId': 'arja_math06',
                          'BugId': 'math06',
                          'PatchedMethods': [{'DevIntention': 'get|method|name',
                                              'OrgCode': 'public void getMethod(int a){ return this.x +a;}',
                                              'PatCode': 'public void getMethod(int a){ return this.x +a;}'}]})


        # triple1 = json.dumps({'DevIntention': 'get method',
        #                        'OrgCode': 'public void getMethod(int a){ return this.x +a;}',
        #                        'PatCode': 'public void getMethod(int a){ return this.x +a;}'})
        # patch_data = [triple1]
        # name = json.dumps(patch_data)
        await websocket.send(msg)
        print(f"> {msg}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())