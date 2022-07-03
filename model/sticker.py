from database import Base
from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from model.sent_sticker import sent_sticker_table


class Sticker(Base):
    __tablename__ = "discord_sticker"

    uid = Column(BigInteger, primary_key=True)

    name = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    url = Column(String, nullable=False)

    messages = relationship(
        "Message", secondary=sent_sticker_table, back_populates="stickers"
    )
