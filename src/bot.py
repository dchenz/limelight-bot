import shlex

import discord

from src.commands import parsing
from src.commands.sync import run_sync_start


class LimelightBot(discord.Client):
    def __init__(self, prefix, allowed_users=None, ignored_channels=None):
        bot_intents = discord.Intents.default()
        bot_intents.messages = True
        super().__init__(intents=bot_intents)
        self.prefix = prefix
        # By default, no users can run commands
        self.allowed_users = set(allowed_users) if allowed_users else set()
        # By default, all channels can be logged if the bot has read permissions
        self.ignored_channels = set(ignored_channels) if ignored_channels else set()

    async def on_ready(self):
        print("----------------")
        print("Bot started")
        print("----------------")
        print(f"Prefix: {self.prefix}")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if message.author.id not in self.allowed_users:  # type: ignore
            return
        if message.guild is None:
            return
        cmd_tokens = shlex.split(message.content)
        if len(cmd_tokens) == 0 or cmd_tokens[0] != self.prefix:
            return
        cmd_tokens = cmd_tokens[1:]
        try:
            args = parsing.parse_command(self.prefix, cmd_tokens)
            if args is None:
                return
        except parsing.CommandParseError as e:
            await message.channel.send(f"Available commands:\n```\n{e.message}\n```")
            return

        if cmd_tokens[:2] == ["sync", "start"]:
            run_sync_start(args, message.guild.text_channels)  # type: ignore
