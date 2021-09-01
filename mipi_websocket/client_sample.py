#!/usr/bin/env python

# WS client example

import asyncio
import json

import websockets


async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        msg = json.dumps({'PatchId': 'patch_sample01',
                          'BugId': 'sample',
                          'PatchedMethods': [{'DevIntention': 'get|max',
                                              'OrgCode': 'public void getMax(int a, int b){ if (a<=b) return a; else return b;}',
                                              'PatCode': 'public void getMax(int a, int b){ if (a>b) return a; else return b;}'}]})

        await websocket.send(msg)
        print(f"> {msg}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())