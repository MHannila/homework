import os

from flask import json
from pymongo import TEXT

from models import Rating, Song


def songs_from_json():
    current_dir = os.getcwd()
    if 'tests' in current_dir:
        current_dir = os.path.join(current_dir, '..')
    current_dir = os.path.join(current_dir, 'src', 'tools')
    with open(os.path.join(current_dir, 'songs.json')) as json_file:
        songs = json.load(json_file)
    assert songs  # Make sure we actually have something
    return songs


def recreate_database():
    Song.collection().drop()
    Rating.collection().drop()
    Song.insert_many(songs_from_json())

    Song.collection().create_index(
        [
            ('artist', TEXT),
            ('title', TEXT),
        ]
    )


if __name__ == '__main__':
    recreate_database()
