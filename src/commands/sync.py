from argparse import Namespace

from src.commands import parsing

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


def show_help(prefix: str) -> str:
    return f"""
{prefix} sync start [--with-channels] [--without-channels]
"""


def parse_args(prefix: str, command: str, argv: list[str]) -> Namespace:
    try:
        if command == "start":
            return _parse_args_start(argv)
    except parsing.CommandParseError:
        pass
    raise parsing.CommandParseError(show_help(prefix))


def _parse_args_start(argv: list[str]) -> Namespace:
    parser = parsing.CommandParser()
    parser.add_argument("--with-channels", nargs="+", required=False)
    parser.add_argument("--without-channels", nargs="+", required=False)
    args = parser.parse_args(argv)
    return args
