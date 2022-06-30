from database import Base
from sqlalchemy import Column, ForeignKey, Integer, Table

message_reacts_table = Table(
    "discord_message_reacts",
    Base.metadata,
    Column("message_id", ForeignKey("discord_message.uid"), primary_key=True),
    Column("emoji_id", ForeignKey("discord_emoji.uid"), primary_key=True),
    Column("count", Integer, nullable=False),
)
