import shlex

import discord

from commands.parsing import CommandParseError
from commands.sync import run_sync_start


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

    def show_commands(self):
        cmds = ("sync start [--with-channels|--without-channels]",)
        return "\n".join(map(lambda s: self.prefix + " " + s, cmds))

    async def on_ready(self):
        print("----------------")
        print("Bot started")
        print("----------------")
        print(f"Prefix: {self.prefix}")
        print("----------------")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if message.author.id not in self.allowed_users:  # type: ignore
            return
        if message.guild is None:
            return
        tokens = shlex.split(message.content)
        if len(tokens) == 0 or tokens[0] != self.prefix:
            return
        try:
            if len(tokens) == 1:
                raise CommandParseError
            if tokens[1] == "sync":
                if len(tokens) == 2:
                    raise CommandParseError
                if tokens[2] == "start":
                    # Remove channels that have been ignored by config
                    channels = [
                        c
                        for c in message.guild.text_channels  # type: ignore
                        if c.id not in self.ignored_channels
                    ]
                    run_sync_start(channels, tokens[3:])
                else:
                    raise CommandParseError
            else:
                raise CommandParseError

        except CommandParseError as e:
            if e.message == "":
                feedback = f"**Commands:**\n```\n{self.show_commands()}\n```"
            else:
                feedback = f"**Error**:\n```\n{e.message}\n```"
            await message.channel.send(feedback)
            return


if __name__ == "__main__":

    import json
    import os

    import dotenv

    def load_discord_ids_config(filename: str) -> list[int]:
        loaded = []
        try:
            with open(filename, "r") as f:
                ids = json.load(f)
                loaded.extend(int(x) for x in ids)
        except FileNotFoundError:
            print("Could not load " + filename)
            exit(1)
        except json.JSONDecodeError:
            pass
        except ValueError:
            print("Invalid ID in " + filename)
            exit(1)
        print(f"Loaded {len(loaded)} from {filename}")
        return loaded

    # Users who can run bot commands
    allowed_users = load_discord_ids_config("config/allowed_users.json")

    # Channels ignored by sync jobs
    # Bot can still listen for commands here
    ignored_channels = load_discord_ids_config("config/ignored_channels.json")

    dotenv.load_dotenv()
    bot = LimelightBot(
        "&lime", allowed_users=allowed_users, ignored_channels=ignored_channels
    )
    token = os.environ.get("TOKEN")
    if not token:
        print("Missing bot token")
        exit(1)
    bot.run(token)
