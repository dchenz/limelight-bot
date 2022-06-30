from database import Base
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship


class Embed(Base):
    __tablename__ = "discord_message_embed"

    uid = Column(Integer, primary_key=True)

    title = Column(String)
    variant = Column(String)
    description = Column(String)
    url = Column(String)
    timestamp = Column(DateTime)
    color = Column(Integer)

    message_id = Column(BigInteger, ForeignKey("discord_message.uid"), nullable=False)
    message = relationship("Message", back_populates="embeds")

    image = relationship("EmbedImage", uselist=False)
    video = relationship("EmbedVideo", uselist=False)
    thumbnail = relationship("EmbedThumbnail", uselist=False)
    provider = relationship("EmbedProvider", uselist=False)
    author = relationship("EmbedAuthor", uselist=False)
    footer = relationship("EmbedFooter", uselist=False)
    fields = relationship("EmbedField")


class EmbedImage(Base):
    __tablename__ = "discord_message_embed_image"

    embed_id = Column(
        Integer, ForeignKey("discord_message_embed.uid"), primary_key=True
    )
    url = Column(String)
    proxy_url = Column(String)
    width = Column(Integer)
    height = Column(Integer)


class EmbedVideo(Base):
    __tablename__ = "discord_message_embed_video"

    embed_id = Column(
        Integer, ForeignKey("discord_message_embed.uid"), primary_key=True
    )
    url = Column(String)
    proxy_url = Column(String)
    width = Column(Integer)
    height = Column(Integer)


class EmbedThumbnail(Base):
    __tablename__ = "discord_message_embed_thumbnail"

    embed_id = Column(
        Integer, ForeignKey("discord_message_embed.uid"), primary_key=True
    )
    url = Column(String)
    proxy_url = Column(String)
    width = Column(Integer)
    height = Column(Integer)


class EmbedProvider(Base):
    __tablename__ = "discord_message_embed_provider"

    embed_id = Column(
        Integer, ForeignKey("discord_message_embed.uid"), primary_key=True
    )
    name = Column(String)
    url = Column(String)


class EmbedAuthor(Base):
    __tablename__ = "discord_message_embed_author"

    embed_id = Column(
        Integer, ForeignKey("discord_message_embed.uid"), primary_key=True
    )
    name = Column(String, nullable=False)
    url = Column(String)
    icon_url = Column(String)
    proxy_icon_url = Column(String)


class EmbedFooter(Base):
    __tablename__ = "discord_message_embed_footer"

    embed_id = Column(
        Integer, ForeignKey("discord_message_embed.uid"), primary_key=True
    )
    text = Column(String, nullable=False)
    url = Column(String)
    icon_url = Column(String)
    proxy_icon_url = Column(String)


class EmbedField(Base):
    __tablename__ = "discord_message_embed_field"

    uid = Column(Integer, primary_key=True)
    embed_id = Column(Integer, ForeignKey("discord_message_embed.uid"))
    name = Column(String, nullable=False)
    value = Column(String)
    inline = Column(Boolean)
