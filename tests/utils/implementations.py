from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional, Sequence, Union

from discord import ChannelType, MessageType


@dataclass
class MockDiscordAsset:
    url: str


@dataclass
class MockDiscordAttachment:
    id: int
    filename: str
    content_type: Optional[str]
    size: int
    url: str
    proxy_url: str
    width: Optional[int]
    height: Optional[int]


@dataclass
class MockDiscordUser:
    id: int
    name: str
    discriminator: str
    bot: bool
    display_avatar: MockDiscordAsset


@dataclass
class MockDiscordColor:
    value: int


@dataclass
class MockDiscordRole:
    id: int
    name: str
    color: MockDiscordColor


@dataclass
class MockDiscordChannel:
    id: int
    type: Optional[ChannelType]


@dataclass
class MockDiscordThread:
    id: int
    name: str
    archived: bool
    type: Optional[ChannelType]


@dataclass
class MockDiscordStickerFormatType:
    name: str


@dataclass
class MockDiscordStickerItem:
    id: int
    name: str
    format: MockDiscordStickerFormatType
    url: str


@dataclass
class MockDiscordEmbedProvider:
    name: Optional[str]
    url: Optional[str]


@dataclass
class MockDiscordEmbedMedia:
    url: Optional[str]
    proxy_url: Optional[str]
    width: Optional[int]
    height: Optional[int]


@dataclass
class MockDiscordEmbedVideo:
    url: Optional[str]
    width: Optional[int]
    height: Optional[int]


@dataclass
class MockDiscordEmbedAuthor:
    name: Optional[str]
    url: Optional[str]
    icon_url: Optional[str]


@dataclass
class MockDiscordEmbedFooter:
    text: Optional[str]
    icon_url: Optional[str]


@dataclass
class MockDiscordEmbedField:
    name: Optional[str]
    value: Optional[str]
    inline: bool


@dataclass
class MockDiscordEmbed:
    title: Optional[str]
    type: str
    description: Optional[str]
    url: Optional[str]
    timestamp: Optional[datetime]
    color: Optional[MockDiscordColor]
    image: Optional[MockDiscordEmbedMedia]
    video: Optional[MockDiscordEmbedVideo]
    thumbnail: Optional[MockDiscordEmbedMedia]
    provider: Optional[MockDiscordEmbedProvider]
    author: Optional[MockDiscordEmbedAuthor]
    footer: Optional[MockDiscordEmbedFooter]
    fields: Sequence[MockDiscordEmbedField]

    def to_dict(self) -> object:
        return vars(self)


@dataclass
class MockDiscordEmoji:
    id: Optional[int]
    name: Optional[str]
    url: Optional[str]


@dataclass
class MockDiscordReaction:
    emoji: Union[MockDiscordEmoji, str]
    count: int


@dataclass
class MockDiscordMessageFlags:
    value: int


@dataclass
class MockDiscordMessageType:
    value: int


@dataclass
class MockDiscordDeletedMessageReference:
    pass


@dataclass
class MockDiscordMessageReference:
    cached_message: Optional["MockDiscordMessage"]
    resolved: Optional[Union["MockDiscordMessage", MockDiscordDeletedMessageReference]]


@dataclass
class MockDiscordMessage:
    id: int
    created_at: datetime
    edited_at: Optional[datetime]
    tts: bool
    mention_everyone: bool
    pinned: bool
    content: str
    jump_url: str
    flags: MockDiscordMessageFlags
    type: MessageType
    author: MockDiscordUser
    channel: MockDiscordChannel
    attachments: Sequence[MockDiscordAttachment]
    mentions: Sequence[MockDiscordUser]
    role_mentions: Sequence[MockDiscordRole]
    channel_mentions: Union[Any, Sequence[Union[MockDiscordChannel, MockDiscordThread]]]
    stickers: Sequence[MockDiscordStickerItem]
    embeds: Sequence[MockDiscordEmbed]
    reactions: Sequence[MockDiscordReaction]
    reference: Optional[MockDiscordMessageReference]


if TYPE_CHECKING:
    from database import interfaces

    a: type[interfaces.DiscordAsset] = MockDiscordAsset
    b: type[interfaces.DiscordAttachment] = MockDiscordAttachment
    c: type[interfaces.DiscordUser] = MockDiscordUser
    d: type[interfaces.DiscordColor] = MockDiscordColor
    e: type[interfaces.DiscordRole] = MockDiscordRole
    f: type[interfaces.DiscordChannel] = MockDiscordChannel
    g: type[interfaces.DiscordThread] = MockDiscordThread
    h: type[interfaces.DiscordStickerFormatType] = MockDiscordStickerFormatType
    i: type[interfaces.DiscordStickerItem] = MockDiscordStickerItem
    j: type[interfaces.DiscordEmbedProvider] = MockDiscordEmbedProvider
    k: type[interfaces.DiscordEmbedMedia] = MockDiscordEmbedMedia
    l: type[interfaces.DiscordEmbedVideo] = MockDiscordEmbedVideo
    m: type[interfaces.DiscordEmbedAuthor] = MockDiscordEmbedAuthor
    n: type[interfaces.DiscordEmbedFooter] = MockDiscordEmbedFooter
    o: type[interfaces.DiscordEmbedField] = MockDiscordEmbedField
    p: type[interfaces.DiscordEmbed] = MockDiscordEmbed
    q: type[interfaces.DiscordEmoji] = MockDiscordEmoji
    r: type[interfaces.DiscordReaction] = MockDiscordReaction
    s: type[interfaces.DiscordMessageFlags] = MockDiscordMessageFlags
    t: type[interfaces.DiscordMessageType] = MockDiscordMessageType
    u: type[
        interfaces.DiscordDeletedMessageReference
    ] = MockDiscordDeletedMessageReference
    v: type[interfaces.DiscordMessageReference] = MockDiscordMessageReference
    w: type[interfaces.DiscordMessage] = MockDiscordMessage
