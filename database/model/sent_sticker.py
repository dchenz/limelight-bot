from sqlalchemy import Column, ForeignKey, Table

from database import Base

# Currently, Discord messages can only have one sticker.
# This may change since the Message.stickers attribute is a list,
# so I'm using a many-to-many relationship for stickers.

sent_sticker_table = Table(
    "discord_sent_sticker",
    Base.metadata,  # type: ignore
    Column("message_id", ForeignKey("discord_message.uid", ondelete="cascade")),
    Column("sticker_id", ForeignKey("discord_sticker.uid")),
)
