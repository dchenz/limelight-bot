from argparse import ArgumentParser


# Prevents the program from exiting on parsing errors
class CommandParser(ArgumentParser):
    def error(self, message: str):
        raise CommandParseError(message)


# Used to store feedback for the bot's user
class CommandParseError(Exception):
    def __init__(self, message: str = ""):
        self.message = message


def get_channel_id(idstr: str) -> int:
    # Tagging a channel results in the ID format "<#1234567890>"
    if idstr.startswith("<#") and idstr.endswith(">"):
        idstr = idstr[2:-1]
    try:
        return int(idstr)
    except ValueError:
        raise CommandParseError(f"Invalid channel ID format: {idstr}")
