from sqlalchemy import Column, ForeignKey, Table

from database import Base

channel_mentions_table = Table(
    "discord_channel_mentions",
    Base.metadata,  # type: ignore
    Column("message_id", ForeignKey("discord_message.uid", ondelete="cascade")),
    Column("channel_id", ForeignKey("discord_channel.uid")),
)
