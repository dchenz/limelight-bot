from database import Base
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        String)
from sqlalchemy.orm import relationship


class Message(Base):
    __tablename__ = "discord_message"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    created_at = Column(DateTime, nullable=False)
    edited_at = Column(DateTime)
    content = Column(String)
    jump_url = Column(String, nullable=False)
    bot = Column(Boolean, nullable=False)

    author_id = Column(BigInteger, ForeignKey("discord_user.uid"), nullable=False)
    author = relationship("User", back_populates="messages")
    channel_id = Column(BigInteger, ForeignKey("discord_channel.uid"), nullable=False)
    channel = relationship("Channel", back_populates="messages")

    embeds = relationship("Embed", back_populates="message")
