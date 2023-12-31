from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from database import DEFAULT_STRING_SIZE, URL_STRING_SIZE, Base
from database.model.sent_sticker import sent_sticker_table


class Sticker(Base):
    __tablename__ = "discord_sticker"

    uid = Column(BigInteger, primary_key=True)

    name = Column(String(DEFAULT_STRING_SIZE), nullable=False)
    content_type = Column(String(DEFAULT_STRING_SIZE), nullable=False)
    url = Column(String(URL_STRING_SIZE), nullable=False)

    messages = relationship(
        "Message",
        secondary=sent_sticker_table,
        back_populates="stickers",
        passive_deletes=True,
    )
