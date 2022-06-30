from database import Base
from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.orm import relationship

from model.role_mentions import role_mentions_table


class Role(Base):
    __tablename__ = "discord_role"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    name = Column(String, nullable=False)
    color = Column(Integer, nullable=False)

    mentions = relationship(
        "Message", secondary=role_mentions_table, back_populates="mention_roles"
    )
