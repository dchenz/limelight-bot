from database import Base
from sqlalchemy import BigInteger, Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from model.reacts_message_emoji import reacts_message_emoji_table


class Emoji(Base):
    __tablename__ = "discord_emoji"

    uid = Column(Integer, primary_key=True)

    custom = Column(Boolean, nullable=False)

    # Not NULL when custom is True
    custom_id = Column(BigInteger)
    custom_name = Column(String)
    custom_url = Column(String)

    # Not NULL when custom is False
    unicode = Column(String)

    messages = relationship(
        "Message", secondary=reacts_message_emoji_table, back_populates="reactions"
    )
