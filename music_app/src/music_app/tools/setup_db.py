from typing import Generator
from pathlib import Path

from flask import json
from pymongo import TEXT

from music_app.models import Rating, Song, MongoItemType


def songs_from_json() -> Generator[MongoItemType, None, None]:
    """Reads the data from the `songs.json` file."""
    json_path = Path(__file__).resolve().parent / 'songs.json'
    with json_path.open() as json_file:
        for line in json_file:
            yield json.loads(line)


def recreate_database() -> None:
    """Drops the collections and repopulates songs from the `songs.json` file."""
    Song.collection().drop()
    Rating.collection().drop()
    Song.insert_many(list(songs_from_json()))

    Song.collection().create_index(
        [
            ('artist', TEXT),
            ('title', TEXT),
        ]
    )


if __name__ == '__main__':
    recreate_database()
