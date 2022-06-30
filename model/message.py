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

from model.mentions_message_channel import mentions_message_channel_table
from model.mentions_message_role import mentions_message_role_table
from model.mentions_message_user import mentions_message_user_table
from model.reacts_message_emoji import reacts_message_emoji_table
from model.sent_message_sticker import sent_message_sticker_table


class Message(Base):
    __tablename__ = "discord_message"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    created_at = Column(DateTime, nullable=False)
    edited_at = Column(DateTime)
    tts = Column(Boolean, nullable=False)
    mention_everyone = Column(Boolean, nullable=False)
    pinned = Column(Boolean, nullable=False)
    content = Column(String)
    jump_url = Column(String, nullable=False)
    bot = Column(Boolean, nullable=False)
    flags = Column(Integer, nullable=False)

    author_id = Column(BigInteger, ForeignKey("discord_user.uid"), nullable=False)
    author = relationship("User", back_populates="messages")
    channel_id = Column(BigInteger, ForeignKey("discord_channel.uid"), nullable=False)
    channel = relationship("Channel", back_populates="messages")

    # Message is a reply if "type" attribute = 19
    # Then, get replied message from "message_reference" attribute
    replying_to_id = Column(BigInteger, ForeignKey("discord_message.uid"))
    replying_to = relationship(
        "Message", back_populates="replied_by", remote_side=[uid]
    )
    replied_by = relationship("Message", back_populates="replying_to")

    mention_users = relationship(
        "User", secondary=mentions_message_user_table, back_populates="mentions"
    )
    mention_roles = relationship(
        "Role", secondary=mentions_message_role_table, back_populates="mentions"
    )
    mention_channels = relationship(
        "Channel", secondary=mentions_message_channel_table, back_populates="mentions"
    )
    embeds = relationship("Embed", back_populates="message")
    attachments = relationship("Attachment", back_populates="message")
    reactions = relationship(
        "Emoji", secondary=reacts_message_emoji_table, back_populates="messages"
    )
    stickers = relationship(
        "Sticker", secondary=sent_message_sticker_table, back_populates="messages"
    )
