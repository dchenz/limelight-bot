from database import Base
from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.orm import relationship

from model.sent_message_sticker import sent_message_sticker_table


class Sticker(Base):
    __tablename__ = "discord_sticker"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    name = Column(String, nullable=False)
    format_type = Column(Integer, nullable=False)
    # URL is None if type is Lottie (2)
    image_url = Column(String)

    messages = relationship(
        "Message", secondary=sent_message_sticker_table, back_populates="stickers"
    )
