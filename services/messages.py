import asyncio

from discord import Message, TextChannel

from database.save import save_discord_message


class MessagesServiceError(Exception):
    def __init__(self, reason: str):
        self.message = reason


class MessagesService:
    def __init__(self):
        self.pending_message_downloads = asyncio.Queue()
        self.pending_channel_downloads = {}
        loop = asyncio.get_event_loop()
        loop.create_task(self._start_worker())

    async def _start_worker(self):
        while True:
            message: Message = await self.pending_message_downloads.get()
            save_discord_message(message)
            self.pending_message_downloads.task_done()

    async def download_message(self, message: Message):
        await self.pending_message_downloads.put(message)

    def download_channel(self, channel: TextChannel):
        if channel.id in self.pending_channel_downloads:
            raise MessagesServiceError("Channel is already being downloaded.")
        loop = asyncio.get_event_loop()
        loop.create_task(self._download_channel(channel))

    async def _download_channel(self, channel: TextChannel):
        self.pending_channel_downloads[channel.id] = channel
        async for message in channel.history(limit=None):
            await self.download_message(message)
        del self.pending_channel_downloads[channel.id]
