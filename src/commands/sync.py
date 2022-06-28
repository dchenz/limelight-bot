import asyncio
from argparse import Namespace

import discord


class SyncController:
    def __init__(self, max_concurrent: int):
        self.sync_sem = asyncio.Semaphore(max_concurrent)

    def start_downloading(self, channels: list[discord.TextChannel]):
        # Check for currently running jobs here
        loop = asyncio.get_event_loop()
        loop.create_task(self._download_channels(channels))

    async def _download_channels(self, channels: list[discord.TextChannel]):
        q = list(channels)
        while q:
            await self.sync_sem.acquire()
            next_channel = q.pop()
            await self._download_channel(next_channel)
            self.sync_sem.release()

    async def _download_channel(self, channel: discord.TextChannel):
        print("downloading", channel.name)


sync_controller = SyncController(max_concurrent=2)


def run_sync_start(args: Namespace, channels: list[discord.TextChannel]):
    queued_channels = []
    for ch in channels:
        included = args.with_channels is None or ch.id in args.with_channels
        excluded = args.without_channels is not None and ch.id in args.without_channels
        if included and not excluded:
            queued_channels.append(ch)
    sync_controller.start_downloading(queued_channels)
