from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, String
from sqlalchemy.orm import relationship

from database import Base
from model.channel_mentions import channel_mentions_table


class Channel(Base):
    """
    This model only supports text channels.
    https://discordpy.readthedocs.io/en/stable/api.html#discord.TextChannel
    """

    __tablename__ = "discord_channel"
    __table_args__ = (
        CheckConstraint("thread is false or (thread_archived is not null)"),
    )

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    name = Column(String, nullable=False)
    thread = Column(Boolean, nullable=False)

    thread_archived = Column(Boolean)

    messages = relationship("Message", back_populates="channel")
    mentions = relationship(
        "Message",
        secondary=channel_mentions_table,
        back_populates="mention_channels",
    )
