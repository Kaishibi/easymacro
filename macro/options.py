import asyncio

class MacroOptions:
    def __init__(self) -> None:
        self.key_delay = 1
        
        self._loop = asyncio.get_event_loop()

    def run_persistently(self) -> None:
        try: self._loop.run_forever()
        finally: self._loop.close()
