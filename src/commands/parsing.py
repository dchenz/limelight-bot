from argparse import ArgumentParser


# Prevents the program from exiting on parsing errors
class CommandParser(ArgumentParser):
    def error(self, message: str):
        raise CommandParseError(message)


# Used to store feedback for the bot's user
class CommandParseError(Exception):
    def __init__(self, message: str = ""):
        self.message = message
