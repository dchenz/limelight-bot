from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from bot.database import Base


class Embed(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#discord.Embed"""

    __tablename__ = "discord_message_embed"

    uid = Column(BigInteger, primary_key=True)

    title = Column(String)
    variant = Column(String)
    description = Column(String)
    url = Column(String)
    timestamp = Column(DateTime)
    color = Column(Integer)

    message_id = Column(BigInteger, ForeignKey("discord_message.uid"), nullable=False)
    image_id = Column(BigInteger, ForeignKey("discord_message_embed_media.uid"))
    video_id = Column(BigInteger, ForeignKey("discord_message_embed_media.uid"))
    thumbnail_id = Column(BigInteger, ForeignKey("discord_message_embed_media.uid"))
    provider_id = Column(BigInteger, ForeignKey("discord_message_embed_provider.uid"))
    author_id = Column(BigInteger, ForeignKey("discord_message_embed_author.uid"))
    footer_id = Column(BigInteger, ForeignKey("discord_message_embed_footer.uid"))

    message = relationship("Message", back_populates="embeds")
    image = relationship("EmbedMedia", uselist=False, foreign_keys=[image_id])
    video = relationship("EmbedMedia", uselist=False, foreign_keys=[video_id])
    thumbnail = relationship("EmbedMedia", uselist=False, foreign_keys=[thumbnail_id])
    provider = relationship("EmbedProvider", uselist=False)
    author = relationship("EmbedAuthor", uselist=False)
    footer = relationship("EmbedFooter", uselist=False)

    fields = relationship("EmbedField")


class EmbedMedia(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#discord.Embed"""

    __tablename__ = "discord_message_embed_media"

    uid = Column(BigInteger, primary_key=True)

    url = Column(String)
    proxy_url = Column(String)
    width = Column(Integer)
    height = Column(Integer)


class EmbedProvider(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#discord.Embed"""

    __tablename__ = "discord_message_embed_provider"

    uid = Column(BigInteger, primary_key=True)

    name = Column(String)
    url = Column(String)


class EmbedAuthor(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#discord.Embed"""

    __tablename__ = "discord_message_embed_author"

    uid = Column(BigInteger, primary_key=True)

    name = Column(String, nullable=False)
    url = Column(String)
    icon_url = Column(String)


class EmbedFooter(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#discord.Embed"""

    __tablename__ = "discord_message_embed_footer"

    uid = Column(BigInteger, primary_key=True)

    text = Column(String, nullable=False)
    icon_url = Column(String)


class EmbedField(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#discord.Embed"""

    __tablename__ = "discord_message_embed_field"

    uid = Column(BigInteger, primary_key=True)

    name = Column(String, nullable=False)
    value = Column(String)
    inline = Column(Boolean)

    embed_id = Column(
        BigInteger, ForeignKey("discord_message_embed.uid"), nullable=False
    )
