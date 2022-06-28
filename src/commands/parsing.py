from argparse import ArgumentParser, Namespace


# Prevents the program from exiting on parsing errors
class CommandParser(ArgumentParser):
    def error(self, message: str):
        raise CommandParseError(message)


# Used to store feedback for the bot's user
class CommandParseError(Exception):
    def __init__(self, message: str = ""):
        self.message = message


def parse_command(prefix: str, tokens: list[str]) -> Namespace:
    """
    Main entrypoint for parsing messages into arguments.
    """
    if len(tokens) == 0:
        raise CommandParseError(available_commands(prefix))
    cmd_type = tokens[0]
    if cmd_type == "sync" and len(tokens) > 1:
        return _parse_sync_args(prefix, tokens[1], tokens[2:])
    raise CommandParseError(available_commands(prefix))


def available_commands(prefix: str) -> str:
    return f"""{_show_sync_help(prefix)}"""


# Command: PREFIX sync
#
# sync start [--with-channels] [--without-channels]
#    - Starts a sync job
# sync jobs [view]
#    - View running sync jobs
# sync jobs cancel
#    - Cancel a running sync job
# sync jobs history
#    - Show past sync jobs


def _show_sync_help(prefix: str) -> str:
    return f"""
{prefix} sync start [--with-channels|--without-channels]
"""


def _parse_sync_args(prefix: str, command: str, argv: list[str]) -> Namespace:
    try:
        if command == "start":
            return _parse_sync_args_start(argv)
    except CommandParseError:
        pass
    raise CommandParseError(_show_sync_help(prefix))


def _parse_sync_args_start(argv: list[str]) -> Namespace:
    parser = CommandParser()
    g1 = parser.add_mutually_exclusive_group()
    g1.add_argument("--with-channels", nargs="+", required=False)
    g1.add_argument("--without-channels", nargs="+", required=False)
    args = parser.parse_args(argv)
    if args.with_channels:
        args.with_channels = [_channel_id_str_to_int(c) for c in args.with_channels]
    if args.without_channels:
        args.without_channels = [
            _channel_id_str_to_int(c) for c in args.without_channels
        ]
    return args


def _channel_id_str_to_int(idstr: str) -> int:
    # Tagging a channel results in the ID format "<#1234567890>"
    if idstr.startswith("<#") and idstr.endswith(">"):
        idstr = idstr[2:-1]
    try:
        return int(idstr)
    except ValueError:
        raise CommandParseError
