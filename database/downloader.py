import asyncio

from discord import Message

from database.save import save_discord_message


class MessageDownloader:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def schedule_download(self, message: Message):
        await self.queue.put(message)

    def start_worker(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self._start_worker())

    async def _start_worker(self):
        while True:
            message: Message = await self.queue.get()
            save_discord_message(message)
            self.queue.task_done()
