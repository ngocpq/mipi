#!/usr/bin/env python

from mipi.mipi_app import Mipi
from mipi_websocket.mipi_server import MipiWSServer

if __name__ == '__main__':
    mipi = Mipi()
    server = MipiWSServer(mipi)
    server.start()
