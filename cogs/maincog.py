from discord import Message
from discord.ext import commands

from database.save import save_discord_message


async def setup(bot: commands.Bot):
    await bot.add_cog(MainCog(bot))


class MainCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("----------------")
        print("Bot started")
        print("----------------")
        print(f"Prefix: {self.bot.command_prefix}")
        print("----------------")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return
        if message.guild is None:
            return
        save_discord_message(message)
