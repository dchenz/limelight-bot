from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.orm import relationship

from bot.database import Base
from bot.model.role_mentions import role_mentions_table


class Role(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#role"""

    __tablename__ = "discord_role"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    name = Column(String, nullable=False)
    color = Column(Integer, nullable=False)

    mentions = relationship(
        "Message", secondary=role_mentions_table, back_populates="mention_roles"
    )
