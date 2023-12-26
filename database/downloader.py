import asyncio
from typing import Union

from discord import Message, TextChannel, Thread

from database.save import save_discord_message


class MessageDownloader:
    def __init__(self):
        self.pending_message_downloads = asyncio.Queue()
        self.pending_channel_downloads = {}
        self.max_concurrent = 3

    async def download_message(self, message: Message):
        await self.pending_message_downloads.put(message)

    def download_channel(self, channel: TextChannel):
        loop = asyncio.get_event_loop()
        loop.create_task(self._download_messages(channel))

    def too_many_channels(self) -> bool:
        return len(self.pending_channel_downloads) >= self.max_concurrent

    def channel_is_downloading(self, channel: TextChannel) -> bool:
        return channel.id in self.pending_channel_downloads

    async def _download_messages(self, t: Union[TextChannel, Thread]):
        self.pending_channel_downloads[t.id] = t
        async for message in t.history(limit=None):
            await self.download_message(message)
        del self.pending_channel_downloads[t.id]

    def start_worker(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self._start_worker())

    async def _start_worker(self):
        while True:
            message: Message = await self.pending_message_downloads.get()
            save_discord_message(message)
            self.pending_message_downloads.task_done()
