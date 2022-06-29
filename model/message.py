from database import Base
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, String


class Message(Base):
    __tablename__ = "discord_message"

    uid = Column(BigInteger, primary_key=True)
    author_id = Column(BigInteger, ForeignKey("discord_user.uid"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    edited_at = Column(DateTime)
    content = Column(String)
    jump_url = Column(String, nullable=False)
    bot = Column(Boolean, nullable=False)
