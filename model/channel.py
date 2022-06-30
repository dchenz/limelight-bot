from database import Base
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        String)
from sqlalchemy.orm import relationship


class Channel(Base):
    __tablename__ = "discord_channel"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    name = Column(String, nullable=False)

    messages = relationship("Message", back_populates="channel")
