import yaml
from schema import Optional, Schema

from bot import LimelightBot
from bot.database import init_database


def load_config():
    config_schema = Schema(
        {
            "token": str,
            "allowed_users": [int],
            Optional("ignored_channels", default=[]): [int],
            "database": {
                "connection_string": str,
                Optional("debug", default=False): bool,
            },
            "bot_prefix": str,
        }
    )
    with open("./config.yaml", "r", encoding="utf-8") as f:
        return config_schema.validate(yaml.safe_load(f))


if __name__ == "__main__":
    config = load_config()
    init_database(
        connection_string=config["database"]["connection_string"],
        debug=config["database"]["debug"],
    )
    bot = LimelightBot(
        prefix=config["bot_prefix"],
        allowed_users=config["allowed_users"],
        ignored_channels=config["ignored_channels"],
    )
    bot.run(config["token"])
