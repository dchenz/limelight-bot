from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.orm import relationship

from database import DEFAULT_STRING_SIZE, Base
from database.model.role_mentions import role_mentions_table


class Role(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#role"""

    __tablename__ = "discord_role"

    # Discord 18-digit ID
    uid = Column(BigInteger, primary_key=True)

    name = Column(String(DEFAULT_STRING_SIZE), nullable=False)
    color = Column(Integer, nullable=False)

    mentions = relationship(
        "Message",
        secondary=role_mentions_table,
        back_populates="mention_roles",
        passive_deletes=True,
    )
