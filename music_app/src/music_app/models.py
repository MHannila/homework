import abc
from typing import Iterable, Any

from bson import ObjectId
from marshmallow import Schema, fields

from music_app.database import init_client

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor

MongoItemValueType = str | int | float | None  # TODO: Non-exhaustive
MongoItemType = dict[str, MongoItemValueType]

class IdField(fields.Field):
    """Field that (de)serialises the MongoDb id
    """

    def _serialize(self, value: ObjectId, *_: Any, **__: Any) -> str:
        return str(value)

    def _deserialize(self, value: str, *_: Any, **__: Any) -> ObjectId:
        return ObjectId(value)


class MongoDbBaseModel(abc.ABC):
    _client = None

    @classmethod
    @abc.abstractmethod
    def collection(cls) -> Collection[MongoItemType]:
        ...

    @classmethod
    def client(cls) -> MongoClient[dict[str, Any]]:
        if cls._client is None:
            cls._client = init_client()
        return cls._client

    @classmethod
    def insert(cls, item: MongoItemType) -> None:
        cls.collection().insert_one(item)

    @classmethod
    def insert_many(cls, songs: Iterable[MongoItemType]) -> None:
        cls.collection().insert_many(songs)

    @classmethod
    def get_all(cls, start_from: int | None = None, limit: int | None = None) -> Cursor[MongoItemType]:
        cursor = cls.collection().find()
        if start_from:
            cursor.skip(start_from)
        if limit:
            cursor.limit(limit)
        return cursor


class Song(MongoDbBaseModel):
    class Schemas:
        class Get(Schema):
            id = IdField(attribute='_id')
            artist = fields.String()
            title = fields.String()
            difficulty = fields.Float()  # TODO: consider changing to Decimal so when doing calculations the results are more precise
            level = fields.Int()
            released = fields.String()  # TODO: change to `fields.Date() after it deserialises to python date on load

    @classmethod
    def collection(cls) -> Collection[MongoItemType]:
        return cls.client().homework.songs


class Rating(MongoDbBaseModel):
    class Schemas:
        class Get(Schema):
            id = IdField(attribute='_id', required=True, allow_none=False)
            song_id = IdField(required=True, allow_none=False)
            rating = fields.Int(required=True, allow_none=False)

        class Post(Get):
            class Meta:
                exclude = ('id',)

    @classmethod
    def collection(cls) -> Collection[MongoItemType]:
        return cls.client().homework.ratings

    @classmethod
    def by_song(cls, song_id: ObjectId) -> Cursor[MongoItemType]:
        return cls.collection().find(dict(song_id=song_id))
