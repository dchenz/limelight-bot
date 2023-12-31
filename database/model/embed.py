from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from database import DEFAULT_STRING_SIZE, URL_STRING_SIZE, Base


class Embed(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#discord.Embed"""

    __tablename__ = "discord_message_embed"

    uid = Column(BigInteger, primary_key=True)

    title = Column(String(DEFAULT_STRING_SIZE))
    variant = Column(String(DEFAULT_STRING_SIZE))
    description = Column(Text)
    url = Column(String(URL_STRING_SIZE))
    timestamp = Column(DateTime)
    color = Column(Integer)

    message_id = Column(
        BigInteger,
        ForeignKey("discord_message.uid", ondelete="cascade"),
        nullable=False,
    )
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

    fields = relationship("EmbedField", back_populates="embed")


class EmbedMedia(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#discord.Embed"""

    __tablename__ = "discord_message_embed_media"

    uid = Column(BigInteger, primary_key=True)

    url = Column(String(URL_STRING_SIZE))
    proxy_url = Column(String(URL_STRING_SIZE))
    width = Column(Integer)
    height = Column(Integer)


class EmbedProvider(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#discord.Embed"""

    __tablename__ = "discord_message_embed_provider"

    uid = Column(BigInteger, primary_key=True)

    name = Column(String(DEFAULT_STRING_SIZE))
    url = Column(String(URL_STRING_SIZE))


class EmbedAuthor(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#discord.Embed"""

    __tablename__ = "discord_message_embed_author"

    uid = Column(BigInteger, primary_key=True)

    name = Column(String(DEFAULT_STRING_SIZE), nullable=False)
    url = Column(String(URL_STRING_SIZE))
    icon_url = Column(String(URL_STRING_SIZE))


class EmbedFooter(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#discord.Embed"""

    __tablename__ = "discord_message_embed_footer"

    uid = Column(BigInteger, primary_key=True)

    text = Column(Text, nullable=False)
    icon_url = Column(String(URL_STRING_SIZE))


class EmbedField(Base):
    """https://discordpy.readthedocs.io/en/stable/api.html#discord.Embed"""

    __tablename__ = "discord_message_embed_field"

    uid = Column(BigInteger, primary_key=True)

    name = Column(String(DEFAULT_STRING_SIZE), nullable=False)
    value = Column(Text)
    inline = Column(Boolean)

    embed_id = Column(
        BigInteger,
        ForeignKey("discord_message_embed.uid", ondelete="cascade"),
        nullable=False,
    )

    embed = relationship("Embed", back_populates="fields")
