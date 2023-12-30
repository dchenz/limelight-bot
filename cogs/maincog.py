import logging
from functools import wraps

from discord import Interaction, Message, app_commands
from discord.ext import commands

from services.messages import MessagesService, MessagesServiceError


async def setup(bot: commands.Bot):
    await bot.add_cog(MainCog(bot))


def log_command(fn):
    @wraps(fn)
    async def _fn(self, interaction: Interaction, *args, **kwargs) -> None:
        logging.info(
            "Received /%s from %s in #%s",
            fn.__name__,
            interaction.user,
            interaction.channel,
        )
        await fn(self, interaction, *args, **kwargs)

    return _fn


class MainCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.messages_svc = MessagesService()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        logging.info("Bot started")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return
        if message.guild is None:
            return
        await self.messages_svc.download_message(message)

    @app_commands.command(description="Download messages in the current channel")
    @log_command
    async def download(self, interaction: Interaction):
        if not interaction.channel:
            return
        try:
            self.messages_svc.download_channel(interaction.channel)
            await interaction.response.send_message("Channel download has started")
        except MessagesServiceError as e:
            await interaction.response.send_message(e.message)

    @app_commands.command(description="Show pending channel downloads")
    @log_command
    async def pending(self, interaction: Interaction):
        channels = self.messages_svc.current_channel_downloads(interaction.guild_id)
        if channels:
            await interaction.response.send_message(
                f"Downloads in progress: {', '.join(c.name for c in channels)}"
            )
        else:
            await interaction.response.send_message("No downloads in progress")
