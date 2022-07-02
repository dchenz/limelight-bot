from database import Base
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from model.channel_mentions import channel_mentions_table
from model.role_mentions import role_mentions_table
from model.sent_sticker import sent_sticker_table
from model.user_mentions import user_mentions_table


class Message(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#message"""

    __tablename__ = "discord_message"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    created_at = Column(DateTime, nullable=False)
    edited_at = Column(DateTime)
    tts = Column(Boolean, nullable=False)
    mention_everyone = Column(Boolean, nullable=False)
    pinned = Column(Boolean, nullable=False)
    content = Column(String, nullable=False)
    jump_url = Column(String, nullable=False)
    flags = Column(Integer, nullable=False)
    variant = Column(Integer, nullable=False)

    author_id = Column(BigInteger, ForeignKey("discord_user.uid"), nullable=False)
    channel_id = Column(BigInteger, ForeignKey("discord_channel.uid"), nullable=False)
    replied_to_id = Column(BigInteger, ForeignKey("discord_message.uid"))
    replied_to_deleted = Column(Boolean, nullable=False)

    author = relationship("User", back_populates="messages")
    channel = relationship("Channel", back_populates="messages")
    replied_to = relationship("Message", back_populates="replied_by", remote_side=[uid])
    replied_by = relationship("Message", back_populates="replied_to")

    embeds = relationship("Embed", back_populates="message")
    attachments = relationship("Attachment", back_populates="message")
    reactions = relationship("Reaction", back_populates="message")

    mention_users = relationship(
        "User", secondary=user_mentions_table, back_populates="mentions"
    )
    mention_roles = relationship(
        "Role", secondary=role_mentions_table, back_populates="mentions"
    )
    mention_channels = relationship(
        "Channel", secondary=channel_mentions_table, back_populates="mentions"
    )
    stickers = relationship(
        "Sticker", secondary=sent_sticker_table, back_populates="messages"
    )
