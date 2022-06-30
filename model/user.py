from database import Base
from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from model.mentions_message_user import mentions_message_user_table


class User(Base):
    __tablename__ = "discord_user"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    username = Column(String, nullable=False, unique=True)
    avatar_url = Column(String)

    messages = relationship("Message", back_populates="author")
    mentions = relationship(
        "Message", secondary=mentions_message_user_table, back_populates="mention_users"
    )
