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
        "database": {
            "connection_string": str,
            Optional("debug", default=False): bool,
        },
    }
)

with open("./config.yaml", "r", encoding="utf-8") as f:
    config = config_schema.validate(yaml.safe_load(f))

init_database(
    connection_string=config["database"]["connection_string"],
    debug=config["database"]["debug"],
)

bot_intents = Intents.default()
bot_intents.messages = True
bot_intents.message_content = True
bot = commands.Bot(command_prefix=None, intents=bot_intents)


@bot.event
async def setup_hook():
    await bot.load_extension("cogs.maincog")


bot.run(config["token"])
