import asyncio
from argparse import Namespace

import discord


class SyncController:
    def __init__(self, max_concurrent: int):
        self.sync_sem = asyncio.Semaphore(max_concurrent)

    def start_downloading(self, channels: list[discord.TextChannel]):
        # Check for currently running jobs here
        # and return immediately
        loop = asyncio.get_event_loop()
        loop.create_task(self._download_channels(channels[::-1]))

    async def _download_channels(self, channels: list[discord.TextChannel]):
        await asyncio.gather(*[self._download_channel(c) for c in channels])

    async def _download_channel(self, channel: discord.TextChannel):
        await self.sync_sem.acquire()
        async for message in channel.history(limit=None):  # type: ignore
            pass  # save messages here
        self.sync_sem.release()

    # async def _download_message(self, )


sync_controller = SyncController(max_concurrent=2)


def run_sync_start(args: Namespace, channels: list[discord.TextChannel]):
    queued_channels = []
    for ch in channels:
        included = args.with_channels is None or ch.id in args.with_channels
        excluded = args.without_channels is not None and ch.id in args.without_channels
        if included and not excluded:
            queued_channels.append(ch)
    sync_controller.start_downloading(queued_channels)
