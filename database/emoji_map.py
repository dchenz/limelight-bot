from zlib import crc32

import discord_emoji as de


def unicode_to_name(u: str) -> str:
    """Get discord emoji name from unicode character"""

    # The function doesn't accept unicode characters
    # It must be an ASCII string with chars [0-255]
    asc_str = "".join(map(chr, bytes(u, "utf-8")))
    names = de.to_discord(asc_str, put_colons=False, get_all=True)
    if not names:
        raise ValueError("Unknown emoji unicode: " + u)
    return names[0]


def unicode_to_asset(u: str) -> str:
    """Get discord emoji asset URL from unicode character"""

    repo = (
        "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/%s.png"
    )
    filename = "-".join(hex(ord(x))[2:] for x in u)
    return repo % (filename,)


def name_to_unicode(name: str) -> str:
    """Get unicode character from discord emoji name"""

    asc_str = de.to_unicode(name)
    if not asc_str:
        raise ValueError("Unknown emoji name: " + name)
    return bytes(map(ord, asc_str)).decode("utf-8")


def name_to_asset(name: str) -> str:
    """Get discord emoji asset URL from discord emoji name"""

    u = name_to_unicode(name)
    return unicode_to_asset(u)


def unicode_to_unique_id(u: str) -> int:
    """Convert unicode character into a unique integer that fits in 8 bytes"""

    # I've tested this and it produces no collisions
    # Hope that new unicode emojis aren't added to Discord!
    return crc32(u.encode("utf-8"))
