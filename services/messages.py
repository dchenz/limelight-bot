import asyncio
from dataclasses import dataclass
from typing import Union

from discord import Message, TextChannel, Thread

from database.queries import delete_discord_message, save_discord_message


class MessagesServiceError(Exception):
    def __init__(self, reason: str):
        self.message = reason


class MessagesService:
    @dataclass
    class DownloadAction:
        message: Message

    @dataclass
    class DeleteAction:
        message_id: int

    def __init__(self):
        self.pending_message_actions: asyncio.Queue[
            Union[MessagesService.DownloadAction, MessagesService.DeleteAction]
        ] = asyncio.Queue()
        self.pending_channel_downloads = {}
        loop = asyncio.get_event_loop()
        loop.create_task(self._start_worker())

    async def _start_worker(self):
        while True:
            action = await self.pending_message_actions.get()
            match action:
                case MessagesService.DownloadAction(message):
                    save_discord_message(message)
                case MessagesService.DeleteAction(message_id):
                    delete_discord_message(message_id)
            self.pending_message_actions.task_done()

    async def download_message(self, message: Message):
        await self.pending_message_actions.put(MessagesService.DownloadAction(message))

    def download_channel(self, channel: Union[TextChannel, Thread]):
        if channel.id in self.pending_channel_downloads:
            raise MessagesServiceError("Channel is already being downloaded.")
        loop = asyncio.get_event_loop()
        loop.create_task(self._download_channel(channel))

    async def _download_channel(self, channel: Union[TextChannel, Thread]):
        self.pending_channel_downloads[channel.id] = channel
        async for message in channel.history(limit=None):
            await self.download_message(message)
        del self.pending_channel_downloads[channel.id]

    def current_channel_downloads(self, guild_id: int) -> list[TextChannel]:
        return [
            channel
            for channel in self.pending_channel_downloads.values()
            if channel.guild.id == guild_id
        ]

    async def delete_message(self, message_id: int):
        await self.pending_message_actions.put(MessagesService.DeleteAction(message_id))
