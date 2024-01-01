import logging

from discord import Intents
from discord.ext import commands

# Required to initialize sqlalchemy models.
# pylint: disable=unused-import
import database.model
from config import load_config
from database import init_database

if __name__ == "__main__":
    config = load_config()

    logging.basicConfig(
        level=logging.getLevelName(config["logging"]["level"].upper()),
        format="%(asctime)s :: %(levelname)s :: %(message)s",
    )

    init_database(
        connection_string=config["database"]["connection_string"],
        debug=config["logging"]["sqlalchemy"],
    )

    bot_intents = Intents.default()
    bot_intents.messages = True
    bot_intents.message_content = True
    bot = commands.Bot(command_prefix="", intents=bot_intents)

    @bot.event
    async def setup_hook():
        await bot.load_extension("cogs.maincog")

    @bot.event
    async def on_command_error(_, error):
        if isinstance(error, commands.CommandNotFound):
            return
        raise error

    bot.run(config["token"])
