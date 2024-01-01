import yaml
from schema import Optional, Schema


def load_config() -> dict:
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
    return config
