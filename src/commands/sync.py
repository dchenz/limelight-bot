import asyncio
from argparse import Namespace

import discord
from src.commands import parsing
from src.utils import get_channel_id_int


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
        print(channel.name)
        # async for message in channel.history(limit=None):  # type: ignore
        #     pass  # save messages here
        self.sync_sem.release()

    # async def _download_message(self, )


sync_controller = SyncController(max_concurrent=2)


def run_sync_start(channels: list[discord.TextChannel], arg_tokens: list[str]):
    args = _parse_sync_start_args(arg_tokens)
    queued_channels = []
    for ch in channels:
        included = args.with_channels is None or ch.id in args.with_channels
        excluded = args.without_channels is not None and ch.id in args.without_channels
        if included and not excluded:
            queued_channels.append(ch)
    sync_controller.start_downloading(queued_channels)


def _parse_sync_start_args(arg_tokens: list[str]) -> Namespace:

    parser = parsing.CommandParser()
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--with-channels", nargs="+", required=False)
    g.add_argument("--without-channels", nargs="+", required=False)
    args = parser.parse_args(arg_tokens)

    # Convert channels to integer ID
    if args.with_channels:
        chs = []
        for ch in args.with_channels:
            cid = get_channel_id_int(ch)
            if cid is None:
                raise parsing.CommandParseError(f"Invalid channel ID format: {ch}")
            chs.append(cid)
        args.with_channels = chs

    # Convert channels to integer ID
    if args.without_channels:
        chs = []
        for ch in args.without_channels:
            cid = get_channel_id_int(ch)
            if cid is None:
                raise parsing.CommandParseError(f"Invalid channel ID format: {ch}")
            chs.append(cid)
        args.without_channels = chs

    return args
