from database import Base
from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "discord_user"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    username = Column(String, nullable=False, unique=True)

    messages = relationship("Message", back_populates="author")
