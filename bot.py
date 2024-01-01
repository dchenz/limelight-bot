import logging
import os

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

# Required to initialize sqlalchemy models.
# pylint: disable=unused-import
import database.model
from config import load_env_boolean, load_env_required
from database import init_database

load_dotenv()

if __name__ == "__main__":
    token = load_env_required("BOT_TOKEN")
    db_connection_string = load_env_required("BOT_DB_CONNECTION_STRING")

    logging.basicConfig(
        level=logging.getLevelName(os.environ.get("BOT_LOG_LEVEL", "ERROR").upper()),
        format="%(asctime)s :: %(levelname)s :: %(message)s",
    )

    init_database(
        connection_string=db_connection_string,
        debug=load_env_boolean("BOT_LOG_SQLALCHEMY"),
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

    bot.run(token)
