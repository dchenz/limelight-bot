from sqlalchemy import Column, ForeignKey, Table

from database import Base

user_mentions_table = Table(
    "discord_user_mentions",
    Base.metadata,
    Column("message_id", ForeignKey("discord_message.uid")),
    Column("user_id", ForeignKey("discord_user.uid")),
)
