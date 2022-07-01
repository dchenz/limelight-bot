from typing import Optional, Union

import discord
import model

from database import Session


def save_discord_message(message: discord.Message):
    """Save a discord message and all of its associated entities"""

    model_message = get_message(message)
    with Session() as session:
        session.merge(model_message)
        session.commit()


def get_message(message: discord.Message) -> model.Message:
    """Convert a discord message into its model object"""

    model_author = get_author(message)
    model_channel = get_channel(message)

    unknown_replied_to = get_replied_to_message(message)
    model_replied_to = None
    replied_to_deleted = False
    if isinstance(unknown_replied_to, discord.Message):
        model_replied_to = get_message(unknown_replied_to)
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


def get_author(message: discord.Message) -> model.User:
    """Convert a discord message's author into its model object"""

    u: discord.User = message.author  # type: ignore
    return model.User(
        uid=u.id,
        username=f"{u.name}#{u.discriminator}",
        bot=u.bot,
        avatar_url=str(u.avatar_url),
    )


def get_channel(message: discord.Message) -> model.Channel:
    """Convert a discord message's channel into its model object"""

    return model.Channel(uid=message.channel.id, name=message.channel.name)


def get_replied_to_message(
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
