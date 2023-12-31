from sqlalchemy import Column, ForeignKey, Table

from database import Base

role_mentions_table = Table(
    "discord_role_mentions",
    Base.metadata,  # type: ignore
    Column("message_id", ForeignKey("discord_message.uid", ondelete="cascade")),
    Column("role_id", ForeignKey("discord_role.uid")),
)
