import asyncio
import threading

from ..settings import BIFROST_API_DROPPER


def start_connection_thread():
    from .connection import connect
    asyncio.get_event_loop()

    t = threading.Thread(target=lambda: asyncio.run(connect()))
    t.setDaemon(True)
    t.start()


connect = lambda: start_connection_thread() if BIFROST_API_DROPPER else None
