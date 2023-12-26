from discord import Interaction, Message, app_commands
from discord.ext import commands

from database.downloader import MessageDownloader


async def setup(bot: commands.Bot):
    await bot.add_cog(MainCog(bot))


class MainCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.message_downloader = MessageDownloader()
        self.message_downloader.start_worker()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print("----------------")
        print("Bot started")
        print("----------------")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return
        if message.guild is None:
            return
        await self.message_downloader.download_message(message)

    @app_commands.command(description="Download messages in the current channel")
    async def download(self, interaction: Interaction):
        if interaction.channel:
            self.message_downloader.download_channel(interaction.channel)
            await interaction.response.send_message("Channel download has started")
