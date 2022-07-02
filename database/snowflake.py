import json
from datetime import datetime
from hashlib import sha1

# Milliseconds since Discord Epoch, the first second of 2015.
DISCORD_EPOCH = 1420070400000

# Not so distant but it's good enough
DISTANT_YEAR = 2040

# Assuming discord doesn't change snowflake structure
# Using 41 bit timestamp instead of 42 bit due to signed integers in Sqlite3.
# Change to 2154 if using other DBMS's that support large integers.
MAX_YEAR = 2084

BIT_MASK_22 = 0x3FFFFF


def hash_to_snowflake(content: str, global_unique: bool = True) -> int:
    """
    Generate an 8-byte Discord snowflake by hashing content.
    Some Discord entities don't have their own IDs;
    this function should be used instead of autoincrementing primary keys
    because they cause objects to be duplicated when downloading more than once
    (downloads should be idempotent).

    If this mock snowflake will exist among real Discord snowflakes
    in the same column, "global_unique" should be set to True.
    This will prevent ID collisions by creating snowflakes with timestamps
    in the distant future, such as 2040/01/01 (see Discord docs).

    Otherwise, if this mock snowflake is independent of real Discord snowflakes
    and the aim is simply to get deterministic IDs, then "global_unique"
    can be set to False. This will generate an 8-byte integer hash of the content.

    https://discord.com/developers/docs/reference#snowflakes
    """

    content_hash = sha1(content.encode("utf-8")).digest()

    if global_unique:
        year = DISTANT_YEAR + int(content_hash[0]) % (MAX_YEAR - DISTANT_YEAR)
        month = 1 + int(content_hash[1]) % 12
        day = 1 + int(content_hash[2]) % 28
        hour = int(content_hash[3]) % 24
        minutes = int(content_hash[4]) % 60
        seconds = int(content_hash[5]) % 60
        distant_future = datetime(year, month, day, hour, minutes, seconds, 0)
        # Bits 64..22 (42 bits)
        snowflake_ts = int(distant_future.timestamp() * 1000) - DISCORD_EPOCH
        # Bits 22..0 (22 bits)
        snowflake_n = int.from_bytes(content_hash[-3:], "big") & BIT_MASK_22
        return (snowflake_ts << 22) | snowflake_n

    return int.from_bytes(content_hash[:8], "big")


def hash_object_to_snowflake(obj) -> int:
    """
    Generate an 8-byte Discord snowflake by hashing the object's representation.
    Raises TypeError if object cannot be hashed.
    """

    rep = json.dumps(obj, sort_keys=True)
    return hash_to_snowflake(rep)
