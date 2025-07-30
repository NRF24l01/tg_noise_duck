from modules import Client, Logger
from asyncio import run
from config import HOST, PORT, API_KEY
from random import choice

class Duck(Client):
    def __init__(self, logger):
        super().__init__(logger)
        
    async def process_message(self, message_type: int, payload: dict, config: dict):
        target_channel = config.get("target_channel", None)
        reactions = config.get("reactions", {})
        chat_id = payload["chat_id"]
        if not target_channel: 
            self.logger.debug("No target channel specified, skipping message processing.")
            return
        if not (type(reactions) is dict and len(reactions.keys()) != 0):
            self.logger.debug("No reactions specified, skipping message processing.")
            return
        if message_type == 1:
            self.logger.debug(f"Received message: {payload}")
            if payload.get("sender").get("type") != "channel" or payload.get("sender").get("id") != target_channel:
                self.logger.debug(f"Message not from target channel, {payload.get('sender').get('id')}!={target_channel}, skipping.")
                return
            answer = self.get_answer(payload.get("message", ""), reactions)
            if answer:
                await self.send_message(chat_id, answer, reply_to=payload["msg_id"])
                self.logger.debug(f"Sent answer: {answer} to chat: {chat_id}")

    def get_answer(self, message: str, reactions: dict):
        for keyword, response in reactions.items():
            if keyword.lower() in message.lower():
                return choice(response)
        return None
        
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
