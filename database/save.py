from typing import Optional, Union

import discord
import model

from database import Session


def save_discord_message(message: discord.Message):
    """Save a discord message and all of its associated entities"""

    model_message = _get_message(message)

    with Session() as session:

        session.merge(model_message)

        for embed in message.embeds:
            e = _get_embed(embed)
            e.message = model_message
            session.merge(e)

        session.commit()


def _get_message(message: discord.Message) -> model.Message:
    """Convert a discord message into its model object"""

    model_author = _get_author(message)
    model_channel = _get_channel(message)

    unknown_replied_to = _get_replied_to_message(message)
    model_replied_to = None
    replied_to_deleted = False
    if isinstance(unknown_replied_to, discord.Message):
        model_replied_to = _get_message(unknown_replied_to)
    elif isinstance(unknown_replied_to, discord.DeletedReferencedMessage):
        replied_to_deleted = True

    model_message = model.Message(
        uid=message.id,
        created_at=message.created_at,
        edited_at=message.edited_at,
        tts=message.tts,
        mention_everyone=message.mention_everyone,
        pinned=message.pinned,
        content=message.content,
        jump_url=message.jump_url,
        flags=message.flags.value,
        variant=message.type.value,
        author=model_author,
        channel=model_channel,
        replied_to=model_replied_to,
        replied_to_deleted=replied_to_deleted,
    )

    return model_message


def _get_author(message: discord.Message) -> model.User:
    """Convert a discord message's author into its model object"""

    u: discord.User = message.author  # type: ignore
    return model.User(
        uid=u.id,
        username=f"{u.name}#{u.discriminator}",
        bot=u.bot,
        avatar_url=str(u.avatar_url),
    )


def _get_channel(message: discord.Message) -> model.Channel:
    """Convert a discord message's channel into its model object"""

    return model.Channel(uid=message.channel.id, name=message.channel.name)


def _get_replied_to_message(
    message: discord.Message,
) -> (Optional[Union[discord.Message, discord.DeletedReferencedMessage]]):
    """
    If a discord message replies to a message,
    convert the other message into its model object
    """

    ref = message.reference
    is_system = message.type != discord.MessageType.default
    if is_system or ref is None:
        return None
    if ref.cached_message:
        return ref.cached_message
    return ref.resolved


def _get_embed(embed: discord.Embed) -> model.Embed:
    """Convert a discord message embed into its model object"""

    model_embed = model.Embed(
        title=_embed_value_or_none(embed.title),
        variant=_embed_value_or_none(embed.type),
        description=_embed_value_or_none(embed.description),
        url=_embed_value_or_none(embed.url),
        timestamp=_embed_value_or_none(embed.timestamp),
    )

    if embed.color:
        model_embed.color = embed.color.value  # type: ignore

    if embed.image:
        model_embed.image = model.EmbedMedia(
            url=_embed_value_or_none(embed.image.url),
            proxy_url=_embed_value_or_none(embed.image.proxy_url),
            width=_embed_value_or_none(embed.image.width),
            height=_embed_value_or_none(embed.image.height),
        )

    if embed.video:
        model_embed.video = model.EmbedMedia(
            url=_embed_value_or_none(embed.video.url),
            proxy_url=_embed_value_or_none(embed.video.proxy_url),
            width=_embed_value_or_none(embed.video.width),
            height=_embed_value_or_none(embed.video.height),
        )

    if embed.thumbnail:
        model_embed.thumbnail = model.EmbedMedia(
            url=_embed_value_or_none(embed.thumbnail.url),
            proxy_url=_embed_value_or_none(embed.thumbnail.proxy_url),
            width=_embed_value_or_none(embed.thumbnail.width),
            height=_embed_value_or_none(embed.thumbnail.height),
        )

    if embed.provider:
        model_embed.provider = model.EmbedProvider(
            name=_embed_value_or_none(embed.provider.name),
            url=_embed_value_or_none(embed.provider.ur),
        )

    if embed.author:
        model_embed.author = model.EmbedAuthor(
            name=_embed_value_or_none(embed.author.name),
            url=_embed_value_or_none(embed.author.url),
            icon_url=_embed_value_or_none(embed.author.icon_url),
            proxy_icon_url=_embed_value_or_none(embed.author.proxy_icon_url),
        )

    if embed.footer:
        model_embed.footer = model.EmbedFooter(
            text=_embed_value_or_none(embed.footer.text),
            url=_embed_value_or_none(embed.footer.url),
            icon_url=_embed_value_or_none(embed.footer.icon_url),
            proxy_icon_url=_embed_value_or_none(embed.footer.proxy_icon_url),
        )

    for field in embed.fields:
        model_embed.fields.append(
            model.EmbedField(name=field.name, value=field.value, inline=field.inline)
        )

    return model_embed


def _embed_value_or_none(embed_value):
    if embed_value == discord.Embed.Empty:
        return None
    return embed_value
