from graphene import List, ObjectType

from database.model import Message
from graphapi.schema import DiscordMessageType
from graphapi.utils import get_graphene_columns


class MessagesQuery(ObjectType):
    graphene_columns = get_graphene_columns(Message)
    messages = List(DiscordMessageType, **graphene_columns)

    def resolve_messages(self, info, **kwargs):
        query = DiscordMessageType.get_query(info)

        for name in MessagesQuery.graphene_columns:
            if name in kwargs:
                query = query.filter(getattr(Message, name) == kwargs.get(name))

        return query.all()
