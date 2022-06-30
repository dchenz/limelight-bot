from database import Base
from sqlalchemy import Column, ForeignKey, Table

mentions_message_user_table = Table(
    "mentions_message_user",
    Base.metadata,
    Column("message_id", ForeignKey("discord_message.uid")),
    Column("user_id", ForeignKey("discord_user.uid")),
)
