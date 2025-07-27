from modules import Client, Logger
from asyncio import Queue, create_task
from asyncio import run, sleep
from time import time
from config import HOST, PORT, API_KEY

class Duck(Client):
    def __init__(self, logger):
        super().__init__(logger)
        
    async def process_message(self, message_type: int, payload: dict, config: dict):
        if message_type == 1:
            self.logger.debug(f"Received message: {payload}")

    def get_loop(self):
        import asyncio
        return asyncio.get_running_loop()

    def stop(self):
        self._worker.stop()

async def main():
    logger = Logger()
    client = Duck(logger)
    await client.init(HOST, PORT, API_KEY)
    await client.polling()

if __name__ == "__main__":
    run(main())
