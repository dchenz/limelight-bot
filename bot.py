import yaml
from schema import Schema
from bot import LimelightBot


def load_config():
    config_schema = Schema(
        {"token": str, "allowed_users": [int], "ignored_channels": [int]}
    )
    with open("./config.yaml") as f:
        return config_schema.validate(yaml.safe_load(f))


if __name__ == "__main__":
    config = load_config()
    bot = LimelightBot(
        "&lime",
        allowed_users=config["allowed_users"],
        ignored_channels=config["ignored_channels"],
    )
    bot.run(config["token"])
