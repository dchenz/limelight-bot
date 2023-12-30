from sqlalchemy import BigInteger, Boolean, Column, String
from sqlalchemy.orm import relationship

from database import DEFAULT_STRING_SIZE, Base


class Emoji(Base):
    __tablename__ = "discord_emoji"

    uid = Column(BigInteger, primary_key=True)

    name = Column(String(DEFAULT_STRING_SIZE), nullable=False)
    url = Column(String(DEFAULT_STRING_SIZE), nullable=False)
    custom = Column(Boolean, nullable=False)

    reactions = relationship("Reaction", back_populates="emoji")
