from database import Base
from sqlalchemy import Column, ForeignKey, Table

# As of now, Discord messages can only have one sticker.
# In case they change this, use a Many-Many relationship.

sent_sticker_table = Table(
    "discord_sent_sticker",
    Base.metadata,
    Column("message_id", ForeignKey("discord_message.uid")),
    Column("sticker_id", ForeignKey("discord_sticker.uid")),
)
