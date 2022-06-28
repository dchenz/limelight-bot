from argparse import ArgumentParser, Namespace

from src.commands import sync


# Prevents the program from exiting on parsing errors
class CommandParser(ArgumentParser):
    def error(self, message: str):
        raise CommandParseError(message)

# Used to store feedback for the bot's user
class CommandParseError(Exception):
    def __init__(self, message: str=""):
        self.message = message


def parse_command(prefix: str, tokens: list[str]) -> Namespace:
    """
    Main entrypoint for parsing messages into arguments.
    """
    if len(tokens) == 0:
        raise CommandParseError(available_commands(prefix))
    cmd_type = tokens[0]
    if cmd_type == "sync" and len(tokens) > 1:
        return sync.parse_args(prefix, tokens[1], tokens[2:])
    raise CommandParseError(available_commands(prefix))


def available_commands(prefix: str) -> str:
    return f"""{sync.show_help(prefix)}"""
