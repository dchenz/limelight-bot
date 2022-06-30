from database import Base
from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from model.channel_mentions import channel_mentions_table


class Channel(Base):
    __tablename__ = "discord_channel"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    name = Column(String, nullable=False)

    messages = relationship("Message", back_populates="channel")
    mentions = relationship(
        "Message",
        secondary=channel_mentions_table,
        back_populates="mention_channels",
    )
