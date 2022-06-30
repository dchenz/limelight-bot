from database import Base
from sqlalchemy import Column, ForeignKey, Integer, Table

reacts_message_emoji_table = Table(
    "reacts_message_emoji",
    Base.metadata,
    Column("message_id", ForeignKey("discord_message.uid"), primary_key=True),
    Column("emoji_id", ForeignKey("discord_emoji.uid"), primary_key=True),
    Column("count", Integer, nullable=False),
)
