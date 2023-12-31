from datetime import datetime
from typing import Any, Optional, Protocol, Sequence, Union

from discord import ChannelType, MessageType


class DiscordAsset(Protocol):
    @property
    def url(self) -> str:
        raise NotImplementedError


class DiscordAttachment(Protocol):
    @property
    def id(self) -> int:
        raise NotImplementedError

    @property
    def filename(self) -> str:
        raise NotImplementedError

    @property
    def content_type(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def size(self) -> int:
        raise NotImplementedError

    @property
    def url(self) -> str:
        raise NotImplementedError

    @property
    def proxy_url(self) -> str:
        raise NotImplementedError

    @property
    def width(self) -> Optional[int]:
        raise NotImplementedError

    @property
    def height(self) -> Optional[int]:
        raise NotImplementedError


class DiscordUser(Protocol):
    """
    Represents Union[discord.Member, discord.User]
    """

    @property
    def id(self) -> int:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def discriminator(self) -> str:
        raise NotImplementedError

    @property
    def bot(self) -> bool:
        raise NotImplementedError

    @property
    def display_avatar(self) -> DiscordAsset:
        raise NotImplementedError


class DiscordColor(Protocol):
    @property
    def value(self) -> int:
        raise NotImplementedError


class DiscordRole(Protocol):
    @property
    def id(self) -> int:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def color(self) -> DiscordColor:
        raise NotImplementedError


class DiscordChannel(Protocol):
    @property
    def id(self) -> int:
        raise NotImplementedError

    @property
    def type(self) -> Optional[ChannelType]:
        raise NotImplementedError

    # This is enforced at runtime due to discord having many channel types.
    # def name(self) -> Optional[str]:
    #     raise NotImplementedError


class DiscordThread(Protocol):
    @property
    def id(self) -> int:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def archived(self) -> bool:
        raise NotImplementedError

    @property
    def type(self) -> Optional[ChannelType]:
        raise NotImplementedError


class DiscordStickerFormatType(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError


class DiscordStickerItem(Protocol):
    @property
    def id(self) -> int:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def format(self) -> DiscordStickerFormatType:
        raise NotImplementedError

    @property
    def url(self) -> str:
        raise NotImplementedError


class DiscordEmbedProvider(Protocol):
    @property
    def name(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def url(self) -> Optional[str]:
        raise NotImplementedError


class DiscordEmbedMedia(Protocol):
    @property
    def url(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def proxy_url(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def width(self) -> Optional[int]:
        raise NotImplementedError

    @property
    def height(self) -> Optional[int]:
        raise NotImplementedError


class DiscordEmbedVideo(Protocol):
    @property
    def url(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def width(self) -> Optional[int]:
        raise NotImplementedError

    @property
    def height(self) -> Optional[int]:
        raise NotImplementedError


class DiscordEmbedAuthor(Protocol):
    @property
    def name(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def url(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def icon_url(self) -> Optional[str]:
        raise NotImplementedError


class DiscordEmbedFooter(Protocol):
    @property
    def text(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def icon_url(self) -> Optional[str]:
        raise NotImplementedError


class DiscordEmbedField(Protocol):
    @property
    def name(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def value(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def inline(self) -> bool:
        raise NotImplementedError


class DiscordEmbed(Protocol):
    @property
    def title(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def type(self) -> str:
        raise NotImplementedError

    @property
    def description(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def url(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def timestamp(self) -> Optional[datetime]:
        raise NotImplementedError

    @property
    def color(self) -> Optional[DiscordColor]:
        raise NotImplementedError

    @property
    def image(self) -> Optional[DiscordEmbedMedia]:
        raise NotImplementedError

    @property
    def video(self) -> Optional[DiscordEmbedVideo]:
        raise NotImplementedError

    @property
    def thumbnail(self) -> Optional[DiscordEmbedMedia]:
        raise NotImplementedError

    @property
    def provider(self) -> Optional[DiscordEmbedProvider]:
        raise NotImplementedError

    @property
    def author(self) -> Optional[DiscordEmbedAuthor]:
        raise NotImplementedError

    @property
    def footer(self) -> Optional[DiscordEmbedFooter]:
        raise NotImplementedError

    @property
    def fields(self) -> Sequence[DiscordEmbedField]:
        raise NotImplementedError

    def to_dict(self) -> object:
        raise NotImplementedError


class DiscordEmoji(Protocol):
    @property
    def id(self) -> Optional[int]:
        raise NotImplementedError

    @property
    def name(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def url(self) -> Optional[str]:
        raise NotImplementedError


class DiscordReaction(Protocol):
    @property
    def emoji(self) -> Union[DiscordEmoji, str]:
        raise NotImplementedError

    @property
    def count(self) -> int:
        raise NotImplementedError


class DiscordMessageFlags(Protocol):
    @property
    def value(self) -> int:
        raise NotImplementedError


class DiscordMessageType(Protocol):
    @property
    def value(self) -> int:
        raise NotImplementedError


class DiscordDeletedMessageReference(Protocol):
    pass


class DiscordMessageReference(Protocol):
    @property
    def cached_message(self) -> Optional["DiscordMessage"]:
        raise NotImplementedError

    @property
    def resolved(
        self,
    ) -> Optional[Union["DiscordMessage", DiscordDeletedMessageReference]]:
        raise NotImplementedError


class DiscordMessage(Protocol):
    @property
    def id(self) -> int:
        raise NotImplementedError

    @property
    def created_at(self) -> datetime:
        raise NotImplementedError

    @property
    def edited_at(self) -> Optional[datetime]:
        raise NotImplementedError

    @property
    def tts(self) -> bool:
        raise NotImplementedError

    @property
    def mention_everyone(self) -> bool:
        raise NotImplementedError

    @property
    def pinned(self) -> bool:
        raise NotImplementedError

    @property
    def content(self) -> str:
        raise NotImplementedError

    @property
    def jump_url(self) -> str:
        raise NotImplementedError

    @property
    def flags(self) -> DiscordMessageFlags:
        raise NotImplementedError

    @property
    def type(self) -> MessageType:
        raise NotImplementedError

    @property
    def author(self) -> DiscordUser:
        raise NotImplementedError

    @property
    def channel(self) -> DiscordChannel:
        raise NotImplementedError

    @property
    def attachments(self) -> Sequence[DiscordAttachment]:
        raise NotImplementedError

    @property
    def mentions(self) -> Sequence[DiscordUser]:
        raise NotImplementedError

    @property
    def role_mentions(self) -> Sequence[DiscordRole]:
        raise NotImplementedError

    @property
    def channel_mentions(
        self,
    ) -> Union[Any, Sequence[Union[DiscordChannel, DiscordThread]]]:
        raise NotImplementedError

    @property
    def stickers(self) -> Sequence[DiscordStickerItem]:
        raise NotImplementedError

    @property
    def embeds(self) -> Sequence[DiscordEmbed]:
        raise NotImplementedError

    @property
    def reactions(self) -> Sequence[DiscordReaction]:
        raise NotImplementedError

    @property
    def reference(self) -> Optional[DiscordMessageReference]:
        raise NotImplementedError
