import asyncio
from argparse import Namespace

import discord
from bot.database.save import save_discord_message
from bot.commands.parsing import CommandParser, get_channel_id


class SyncController:
    """
    Controls the scheduing of channel being downloaded
    and ensures that no more than the configured limit
    are running concurrently.
    """

    def __init__(self, max_concurrent: int):
        self.max_concurrent = max_concurrent
        self.sync_lock = asyncio.Lock()

    def start_downloading(self, channels: list[discord.TextChannel]):
        # Check for currently running jobs here
        # and return immediately
        loop = asyncio.get_event_loop()
        loop.create_task(self._download_channels(channels))

    async def _download_channels(self, channels: list[discord.TextChannel]):
        if self.sync_lock.locked():
            return
        await self.sync_lock.acquire()
        print("starting download sync")
        sync_sem = asyncio.Semaphore(self.max_concurrent)
        await asyncio.gather(*[self._download_channel(c, sync_sem) for c in channels])
        self.sync_lock.release()
        print("done")

    async def _download_channel(
        self, channel: discord.TextChannel, sem: asyncio.Semaphore
    ):
        await sem.acquire()
        print("downloading", channel.name)
        async for message in channel.history(limit=None):
            save_discord_message(message)
        for thread in channel.threads:
            print("- downloading", thread.name)
            async for message in thread.history(limit=None):
                save_discord_message(message)
            print("- finished", thread.name)
        sem.release()
        print("finished", channel.name)


sync_controller = SyncController(max_concurrent=2)


def run_sync_start(channels: list[discord.TextChannel], arg_tokens: list[str]):
    """
    Starts a sync job to download messages from a list of channels.
    Arguments can specify --with-channels or --without-channels
    to select certain channels from this list to include/exclude.
    """

    args = _parse_sync_start_args(arg_tokens)
    queued_channels = []
    for ch in channels:
        included = args.with_channels is None or ch.id in args.with_channels
        excluded = args.without_channels is not None and ch.id in args.without_channels
        if included and not excluded:
            queued_channels.append(ch)
    sync_controller.start_downloading(queued_channels)


def _parse_sync_start_args(arg_tokens: list[str]) -> Namespace:
    """
    Validates command arguments received from the user
    and normalises channel IDs into integers.
    """

    parser = CommandParser()
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--with-channels", nargs="+", required=False)
    g.add_argument("--without-channels", nargs="+", required=False)
    args = parser.parse_args(arg_tokens)

    # Convert channels to integer ID
    if args.with_channels:
        args.with_channels = [get_channel_id(c) for c in args.with_channels]

    # Convert channels to integer ID
    if args.without_channels:
        args.without_channels = [get_channel_id(c) for c in args.without_channels]

    return args
