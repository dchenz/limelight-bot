from sqlalchemy import BigInteger, Boolean, Column, String
from sqlalchemy.orm import relationship

from database import DEFAULT_STRING_SIZE, URL_STRING_SIZE, Base
from model.user_mentions import user_mentions_table


class User(Base):
    """
    https://discordpy.readthedocs.io/en/stable/api.html#discord.abc.User
    https://discordpy.readthedocs.io/en/stable/api.html#discord.Member
    """

    __tablename__ = "discord_user"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    username = Column(String(DEFAULT_STRING_SIZE), nullable=False, unique=True)
    bot = Column(Boolean, nullable=False)
    avatar_url = Column(String(URL_STRING_SIZE), nullable=False)

    messages = relationship("Message", back_populates="author")
    mentions = relationship(
        "Message", secondary=user_mentions_table, back_populates="mention_users"
    )
