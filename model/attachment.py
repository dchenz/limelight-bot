from database import Base
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Attachment(Base):
    __tablename__ = "discord_message_attachment"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    filename = Column(String, nullable=False)
    description = Column(String)
    content_type = Column(String)
    size = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    proxy_url = Column(String, nullable=False)
    width = Column(Integer)
    height = Column(Integer)

    message_id = Column(BigInteger, ForeignKey("discord_message.uid"), nullable=False)
    message = relationship("Message", back_populates="attachments")