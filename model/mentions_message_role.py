from database import Base
from sqlalchemy import Column, ForeignKey, Table

mentions_message_role_table = Table(
    "mentions_message_role",
    Base.metadata,
    Column("message_id", ForeignKey("discord_message.uid")),
    Column("role_id", ForeignKey("discord_role.uid")),
)
