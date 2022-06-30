from database import Base
from sqlalchemy import Column, ForeignKey, Table

# As of now, Discord messages can only have one sticker.
# In case they change this, use a Many-Many relationship.

sent_message_sticker_table = Table(
    "sent_message_sticker",
    Base.metadata,
    Column("message_id", ForeignKey("discord_message.uid")),
    Column("sticker_id", ForeignKey("discord_sticker.uid")),
)
