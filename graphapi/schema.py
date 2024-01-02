from typing import Optional

from graphene.types import String
from graphene_sqlalchemy import SQLAlchemyObjectType

from database import model


class DiscordMessageType(SQLAlchemyObjectType):
    uid = String()
    author_id = String()
    channel_id = String()
    reference_id = String()

    class Meta:
        model = model.Message

    def resolve_uid(self, _) -> str:
        return str(self.uid)

    def resolve_author_id(self, _) -> str:
        return str(self.author_id)

    def resolve_channel_id(self, _) -> str:
        return str(self.channel_id)

    def resolve_reference_id(self, _) -> Optional[str]:
        if not self.reference_id:
            return None
        return str(self.reference_id)
