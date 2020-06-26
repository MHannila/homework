from typing import Dict, Iterable

from bson import ObjectId
from marshmallow import Schema, fields

import database


class IdField(fields.Field):
    """Field that (de)serialises the MongoDb id
    """

    def _serialize(self, value, *_, **__):
        return str(value)

    def _deserialize(self, value, *_, **__):
        return ObjectId(value)


class MongoDbBaseModel:
    @classmethod
    def insert(cls, rating: Dict):
        cls.collection().insert_one(rating)

    @classmethod
    def insert_many(cls, songs: Iterable):
        cls.collection().insert_many(songs)

    @classmethod
    def get_all(cls, start_from: int = None, limit: int = None):
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

    @staticmethod  # TODO: make class property
    def collection():
        return database.client().homework.songs


class Rating(MongoDbBaseModel):
    class Schemas:
        class Get(Schema):
            id = IdField(attribute='_id', required=True, allow_none=False)
            song_id = IdField(required=True, allow_none=False)
            rating = fields.Int(required=True, allow_none=False)

        class Post(Get):
            class Meta:
                exclude = ('id',)

    @staticmethod  # TODO: make class property
    def collection():
        return database.client().homework.ratings

    @classmethod
    def by_song(cls, song_id: ObjectId):
        return cls.collection().find(dict(song_id=song_id))
