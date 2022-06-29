from typing import Optional


def get_channel_id_int(idstr: str) -> Optional[int]:
    # Tagging a channel results in the ID format "<#1234567890>"
    if idstr.startswith("<#") and idstr.endswith(">"):
        idstr = idstr[2:-1]
    try:
        return int(idstr)
    except ValueError:
        return None
