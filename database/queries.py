from typing import TYPE_CHECKING, Optional, Union

import discord_emoji
from discord import ChannelType

from database import Session, model, snowflake

if TYPE_CHECKING:
    from database.interfaces import (
        DiscordAttachment,
        DiscordChannel,
        DiscordEmbed,
        DiscordEmbedMedia,
        DiscordEmbedVideo,
        DiscordEmoji,
        DiscordMessage,
        DiscordMessageReference,
        DiscordReaction,
        DiscordRole,
        DiscordStickerItem,
        DiscordUser,
    )


def save_discord_message(message: "DiscordMessage"):
    """Save a discord message and all of its associated entities"""

    model_message = _get_message(message)

    for atch in message.attachments:
        model_message.attachments.append(_get_attachment(atch))

    for user in message.mentions:
        model_message.mention_users.append(_get_user(user))

    for role in message.role_mentions:
        model_message.mention_roles.append(_get_role(role))

    for channel in message.channel_mentions:
        model_message.mention_channels.append(_get_channel(channel))

    for sticker in message.stickers:
        model_message.stickers.append(_get_sticker(sticker))

    for embed in message.embeds:
        model_message.embeds.append(_get_embed(embed))

    with Session() as session:
        session.merge(model_message)

        # Does not work if reaction PK already added to db
        session.query(model.Reaction).filter(
            model.Reaction.message_id == model_message.uid
        ).delete()
        for react in message.reactions:
            r = _get_reaction(react, model_message)
            session.merge(r)

        session.commit()


def _get_message(message: "DiscordMessage") -> model.Message:
    """Convert a discord message into its model object"""

    reference = None
    if message.reference is not None:
        reference = _get_message_ref(message.reference)

    model_message = model.Message(  # type: ignore
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
        author=_get_user(message.author),
        channel=_get_channel(message.channel),
        reference=reference,
    )

    return model_message


def _get_user(user: "DiscordUser") -> model.User:
    """Convert a discord message's author into its model object"""

    return model.User(  # type: ignore
        uid=user.id,
        username=f"{user.name}#{user.discriminator}",
        bot=user.bot,
        avatar_url=user.display_avatar.url,
    )


def _get_channel(channel: "DiscordChannel") -> model.Channel:
    """Convert a discord message's channel/thread into its model object"""

    name = getattr(channel, "name", None)
    if name is None:
        raise ValueError("Unsupported object: " + str(channel))

    return model.Channel(  # type: ignore
        uid=channel.id,
        name=name,
        thread=channel.type in (ChannelType.public_thread, ChannelType.private_thread),
        thread_archived=getattr(channel, "archived", None),
    )


def _get_message_ref(ref: "DiscordMessageReference") -> Optional[model.Message]:
    """Convert a discord message's reference into its model object"""

    if ref.cached_message is not None:
        return _get_message(ref.cached_message)
    if ref.resolved and hasattr(ref.resolved, "author"):
        return _get_message(ref.resolved)  # type: ignore Deleted messages have no author
    return None


def _get_sticker(sticker: "DiscordStickerItem") -> model.Sticker:
    """Convert a discord sticker into its model object"""

    return model.Sticker(  # type: ignore
        uid=sticker.id,
        name=sticker.name,
        content_type=sticker.format.name,
        url=sticker.url,
    )


def _get_embed(embed: "DiscordEmbed") -> model.Embed:
    """Convert a discord message embed into its model object"""

    # This ID will be shared across some embed subtables,
    # such as model.EmbedFooter, because they are 1-1 mapping
    # and only exist if model.Embed exists.
    embed_unique_id = snowflake.hash_object_to_snowflake(
        embed.to_dict(), global_unique=False
    )

    model_embed = model.Embed(  # type: ignore
        uid=embed_unique_id,
        title=embed.title,
        variant=embed.type,
        description=embed.description,
        url=embed.url,
        timestamp=embed.timestamp,
    )

    if embed.color:
        model_embed.color = embed.color.value

    if embed.image:
        model_embed.image = _get_embed_media(embed.image)

    if embed.video:
        model_embed.video = _get_embed_media(embed.video)

    if embed.thumbnail:
        model_embed.thumbnail = _get_embed_media(embed.thumbnail)

    if embed.provider:
        model_embed.provider = model.EmbedProvider(  # type: ignore
            uid=embed_unique_id,
            name=embed.provider.name,
            url=embed.provider.url,
        )

    if embed.author:
        model_embed.author = model.EmbedAuthor(  # type: ignore
            uid=embed_unique_id,
            name=embed.author.name,
            url=embed.author.url,
            icon_url=embed.author.icon_url,
        )

    if embed.footer:
        model_embed.footer = model.EmbedFooter(  # type: ignore
            uid=embed_unique_id,
            text=embed.footer.text,
            icon_url=embed.footer.icon_url,
        )

    for field in embed.fields:
        model_embed.fields.append(
            model.EmbedField(  # type: ignore
                uid=snowflake.hash_object_to_snowflake(
                    [field.name, field.value, field.inline], global_unique=False
                ),
                name=field.name,
                value=field.value,
                inline=field.inline,
            )
        )

    return model_embed


def _get_embed_media(
    media: "Union[DiscordEmbedMedia, DiscordEmbedVideo]",
) -> model.EmbedMedia:
    obj = [
        getattr(media, "url", None),
        getattr(media, "proxy_url", None),
        getattr(media, "width", None),
        getattr(media, "height", None),
    ]
    return model.EmbedMedia(  # type: ignore
        uid=snowflake.hash_object_to_snowflake(obj, global_unique=False),
        url=obj[0],
        proxy_url=obj[1],
        width=obj[2],
        height=obj[3],
    )


def _get_attachment(attachment: "DiscordAttachment") -> model.Attachment:
    """Convert a discord message attachment into its model object"""

    return model.Attachment(  # type: ignore
        uid=attachment.id,
        filename=attachment.filename,
        content_type=attachment.content_type,
        size=attachment.size,
        url=attachment.url,
        proxy_url=attachment.proxy_url,
        width=attachment.width,
        height=attachment.height,
    )


def _get_role(role: "DiscordRole") -> model.Role:
    """Convert a discord role into its model object"""

    return model.Role(  # type: ignore
        uid=role.id, name=role.name, color=role.color.value
    )


def _get_reaction(
    reaction: "DiscordReaction", model_message: model.Message
) -> model.Reaction:
    """Convert a discord reaction into its model object"""

    model_emoji = _get_emoji(reaction.emoji)

    model_react = model.Reaction(  # type: ignore
        message=model_message, emoji=model_emoji, count=reaction.count
    )

    return model_react


def _get_emoji(emoji: "Union[DiscordEmoji, str]") -> model.Emoji:
    """Convert a discord emoji into its model object"""

    if isinstance(emoji, str):
        # Unicode emojis will exist in same table as custom emojis which have real snowflakes
        emoji_id = snowflake.hash_to_snowflake(emoji, global_unique=True)
        emoji_name = discord_emoji.unicode_to_name(emoji)
        emoji_url = discord_emoji.unicode_to_image(emoji)
        is_custom = False
    else:
        emoji_id = emoji.id
        emoji_name = emoji.name
        emoji_url = emoji.url
        is_custom = True

    return model.Emoji(  # type: ignore
        uid=emoji_id, name=emoji_name, url=emoji_url, custom=is_custom
    )


def delete_discord_message(message_id: int):
    with Session() as session:
        model_message = session.query(model.Message).filter(
            model.Message.uid == message_id
        )
        model_message.delete()
        session.commit()
