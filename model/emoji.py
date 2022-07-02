from database import Base
from sqlalchemy import BigInteger, Boolean, Column, String
from sqlalchemy.orm import relationship


class Emoji(Base):
    __tablename__ = "discord_emoji"

    # For custom emojis, this is Discord's 18-digit ID.
    # For default emojis, this is a hash of its unicode value(s).
    uid = Column(BigInteger, primary_key=True)

    name = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False)
    custom = Column(Boolean, nullable=False)

    reactions = relationship("Reaction", back_populates="emoji")
