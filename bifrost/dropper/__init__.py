import asyncio
import threading

from ..settings import BIFROST_API_DROPPER
from .connection import connect as _connect


def start_connection_thread():
    asyncio.get_event_loop()

    t = threading.Thread(target=lambda: asyncio.run(_connect()))
    t.setDaemon(True)
    t.start()


connect = lambda: start_connection_thread() if BIFROST_API_DROPPER else None
