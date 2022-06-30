from database import Base
from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from model.mentions_message_channel import mentions_message_channel_table


class Channel(Base):
    __tablename__ = "discord_channel"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    name = Column(String, nullable=False)

    messages = relationship("Message", back_populates="channel")
    mentions = relationship(
        "Message",
        secondary=mentions_message_channel_table,
        back_populates="mention_channels",
    )
