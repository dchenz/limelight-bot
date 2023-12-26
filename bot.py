import yaml
from schema import Schema
from bot import LimelightBot
from database import init_database


def load_config():
    config_schema = Schema(
        {
            "token": str,
            "allowed_users": [int],
            "ignored_channels": [int],
            "database": {"connection_string": str, "debug": bool},
        }
    )
    with open("./config.yaml") as f:
        return config_schema.validate(yaml.safe_load(f))


if __name__ == "__main__":
    config = load_config()
    init_database(
        connection_string=config["database"]["connection_string"],
        debug=config["database"]["debug"],
    )
    bot = LimelightBot(
        "&lime",
        allowed_users=config["allowed_users"],
        ignored_channels=config["ignored_channels"],
    )
    bot.run(config["token"])
