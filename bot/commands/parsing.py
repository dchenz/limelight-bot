from argparse import ArgumentParser


class CommandParser(ArgumentParser):
    """Argparse wrapper that prevents errors from exiting the program"""

    def error(self, message: str):
        raise CommandParseError(message)


class CommandParseError(Exception):
    """Error used to store feedback for the bot's user"""

    def __init__(self, message: str = ""):
        self.message = message


def get_channel_id(idstr: str) -> int:
    """
    Converts a channel ID string into an integer.
    Channel mentions are also supported in the format of "<#1234567890>".
    """

    if idstr.startswith("<#") and idstr.endswith(">"):
        idstr = idstr[2:-1]
    try:
        return int(idstr)
    except ValueError:
        raise CommandParseError(f"Invalid channel ID format: {idstr}")
