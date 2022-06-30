from database import Base
from sqlalchemy import BigInteger, Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from model.message_reacts import message_reacts_table


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
        "Message", secondary=message_reacts_table, back_populates="reactions"
    )
