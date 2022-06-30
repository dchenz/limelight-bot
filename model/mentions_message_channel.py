from database import Base
from sqlalchemy import Column, ForeignKey, Table

mentions_message_channel_table = Table(
    "mentions_message_channel",
    Base.metadata,
    Column("message_id", ForeignKey("discord_message.uid")),
    Column("channel_id", ForeignKey("discord_channel.uid")),
)
