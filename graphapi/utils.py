from typing import TYPE_CHECKING

from graphene import BigInt as GrapheneBigInt
from graphene import Boolean as GrapheneBoolean
from graphene import DateTime as GrapheneDatetime
from graphene import Int as GrapheneInt
from graphene import String as GrapheneString
from sqlalchemy.inspection import inspect
from sqlalchemy.types import BigInteger as SQLBigInt
from sqlalchemy.types import Boolean as SQLBoolean
from sqlalchemy.types import DateTime as SQLDatetime
from sqlalchemy.types import Integer as SqlInt
from sqlalchemy.types import String as SQLString
from sqlalchemy.types import Text as SQLText

if TYPE_CHECKING:
    from graphene.types.base import BaseType


def _map_column_type(column_type) -> "BaseType":
    if isinstance(column_type, (SQLString, SQLText)):
        return GrapheneString()
    if isinstance(column_type, SQLBigInt):
        return GrapheneBigInt()
    if isinstance(column_type, SqlInt):
        return GrapheneInt()
    if isinstance(column_type, SQLBoolean):
        return GrapheneBoolean()
    if isinstance(column_type, SQLDatetime):
        return GrapheneDatetime()
    raise ValueError(f"Unsupported column type: {column_type}")


def get_graphene_columns(model) -> dict[str, "BaseType"]:
    result = inspect(model, raiseerr=True)
    assert result is not None
    return {
        name: _map_column_type(column.type) for (name, column) in result.columns.items()
    }
