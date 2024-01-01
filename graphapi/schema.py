from graphene_sqlalchemy import SQLAlchemyObjectType

from database import model


class DiscordMessageType(SQLAlchemyObjectType):
    class Meta:
        model = model.Message
