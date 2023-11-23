import datetime
import typing
from typing import Any, Callable

from pydantic_core import core_schema

from src.pydantic_mongo.exceptions import TypingStub

E = typing.TypeVar('E')


class MongoList(list, typing.Generic[E]):

    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            _source_type: Any,
            _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        return core_schema.list_schema()

    @property
    def list_elem(self) -> E:
        raise TypingStub


class MongoType:
    @property
    def validation_alias(self) -> typing.Self:
        """For type hints in usage"""
        raise TypingStub

    def __getitem__(self, item) -> typing.Self:
        """
        Allows usage of this item as element in typing
        union with get path by matching element, not first from list
        """
        raise TypingStub


class MongoDT(datetime.datetime, MongoType):
    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            _source_type: Any,
            _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        return core_schema.datetime_schema()
