import os


class ConfigError(Exception):
    pass


def load_env_required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ConfigError(f"Missing environment variable: {name}")
    return value


def load_env_boolean(name: str, default_value=False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default_value
    return value.lower() in ("1", "true", "yes")
