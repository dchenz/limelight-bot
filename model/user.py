from database import Base
from sqlalchemy import BigInteger, Column, String


class User(Base):
    __tablename__ = "discord_user"

    uid = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=False, unique=True)
