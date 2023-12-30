from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import DEFAULT_STRING_SIZE, URL_STRING_SIZE, Base


class Attachment(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#attachment"""

    __tablename__ = "discord_message_attachment"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    filename = Column(String(DEFAULT_STRING_SIZE), nullable=False)
    content_type = Column(String(DEFAULT_STRING_SIZE))
    size = Column(Integer, nullable=False)
    url = Column(String(URL_STRING_SIZE), nullable=False)
    proxy_url = Column(String(URL_STRING_SIZE), nullable=False)
    width = Column(Integer)
    height = Column(Integer)

    message_id = Column(BigInteger, ForeignKey("discord_message.uid"), nullable=False)

    message = relationship("Message", back_populates="attachments")
