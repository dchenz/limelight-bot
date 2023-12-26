from bot.database import Base
from sqlalchemy import BigInteger, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Reaction(Base):
    __tablename__ = "discord_message_reaction"

    message_id = Column(BigInteger, ForeignKey("discord_message.uid"), primary_key=True)
    emoji_id = Column(BigInteger, ForeignKey("discord_emoji.uid"), primary_key=True)

    message = relationship("Message", back_populates="reactions")
    emoji = relationship("Emoji", back_populates="reactions")

    count = Column(Integer, nullable=False)
