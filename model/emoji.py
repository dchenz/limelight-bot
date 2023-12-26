from sqlalchemy import BigInteger, Boolean, Column, String
from sqlalchemy.orm import relationship

from database import Base


class Emoji(Base):
    __tablename__ = "discord_emoji"

    uid = Column(BigInteger, primary_key=True)

    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    custom = Column(Boolean, nullable=False)

    reactions = relationship("Reaction", back_populates="emoji")
