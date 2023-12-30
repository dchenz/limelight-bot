import logging

import yaml
from discord import Intents
from discord.ext import commands
from schema import Optional, Schema

# Required to initialize sqlalchemy models.
# pylint: disable=unused-import
import model
from database import init_database

config_schema = Schema(
    {
        "token": str,
        Optional("logging"): {
            Optional("level", default="ERROR"): str,
            Optional("sqlalchemy", default=False): bool,
        },
        "database": {
            "connection_string": str,
        },
    }
)


with open("./config.yaml", "r", encoding="utf-8") as f:
    config = config_schema.validate(yaml.safe_load(f))
    if "logging" not in config:
        config["logging"] = {"level": "ERROR", "sqlalchemy": False}

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
