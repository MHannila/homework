import random
import statistics

import mongomock

import pytest
from faker import Faker

from ..src import database
from ..src.models import Rating, Song
from ..src.tools.setup_db import recreate_database, songs_from_json

fake = Faker()

songs = songs_from_json()


@mongomock.patch((f'mongodb://{database.HOST}:{database.PORT}/'))
class TestSongsAPI:
    def test_get_songs(self, client):
        recreate_database()

        r = client.get('/songs')
        assert r.status_code == 200
        assert len(r.json['results']) == len(songs)
        for song in songs:
            found = False
            for r_song in r.json['results']:
                if all(attr_value == song[attr_name] for attr_name, attr_value in r_song.items() if attr_name != 'id'):
                    found = True
                    break
            assert found, 'a song from the json not returned'

    def test_get_songs_paginated(self, client):
        recreate_database()

        page_size = random.randint(3, 6)

        r = client.get(f'/songs?limit={page_size}')
        assert r.status_code == 200
        assert len(r.json['results']) == page_size
        next = r.json['next_start']

        while next:
            r = client.get(f'/songs?limit={page_size}&start_from={next}')
            assert r.status_code == 200

            try:
                next = r.json['next_start']
                assert len(r.json['results']) == page_size
            except KeyError:
                next = None
                assert len(r.json['results']) <= page_size

    def test_get_songs_avg_diff(self, client):
        recreate_database()

        r = client.get(f'/songs/avg/difficulty')
        assert r.status_code == 200
        assert r.json['average_difficulty'] == statistics.mean([x['difficulty'] for x in Song.get_all()])

    def test_get_songs_avg_diff_by_level(self, client):
        recreate_database()

        all_songs = list(Song.get_all())
        all_levels = [song['level'] for song in all_songs]
        rand_level = random.choice(all_levels)
        r = client.get(f'/songs/avg/difficulty?level={rand_level}')
        assert r.status_code == 200
        assert r.json['average_difficulty'] == statistics.mean([x['difficulty'] for x in all_songs if x['level'] == rand_level])

    @pytest.mark.skip(reason='NotImplementedError: The $text operator is not implemented in mongomock yet')
    def test_get_songs_search(self, client):
        recreate_database()

        # Create new songs with random artist and title that we can then search for
        rand_title_words = fake.words(nb=4)
        rand_title_word = random.choice(rand_title_words)
        title_id = Song.insert(dict(
            title=' '.join(rand_title_words)
        ))

        rand_artist_words = fake.words(nb=4)
        rand_artist_word = random.choice(rand_artist_words)
        artist_id = Song.insert(dict(
            artist=' '.join(rand_artist_words)
        ))

        for search_term, id in ((rand_title_word, title_id), (rand_artist_word, artist_id)):
            r = client.get(f'/songs/search?term={search_term}')
            assert r.status_code == 200
            assert len(r.json['results']) == 1
            assert r.json['results'][0]['id'] == id

    @pytest.mark.parametrize('missing', ('song_id', 'rating'))
    def test_new_rating_missing_values(self, client, missing):
        recreate_database()

        song = random.choice(list(Song.get_all()))
        data = dict(song_id=str(song['_id']), rating=1)
        data.pop(missing)
        r = client.post('/songs/rating', json=data)
        assert r.status_code == 400
        assert 'Missing data for required field.' in r.json['errors'][missing]

    def test_songs_ratings(self, client):
        recreate_database()

        # Add new random ratings
        new_ratings = [random.randint(1, 5) for _ in range(3)]  # Small sample to avoid min/max always being 1 & 5
        song = random.choice(list(Song.get_all()))
        song_ratings = len(list(Rating.by_song(song['_id'])))
        for rating in new_ratings:
            r = client.post('/songs/rating', json=dict(song_id=str(song['_id']), rating=rating))
            assert r.status_code == 200
            song_ratings += 1
            assert len(list(Rating.by_song(song['_id']))) == song_ratings

        # Check average, min, and max ratings from the ones just added
        r = client.get(f'/songs/avg/rating/{song["_id"]}')
        assert r.status_code == 200
        assert r.json['average_rating'] == statistics.mean(new_ratings)
        assert r.json['min_rating'] == min(new_ratings)
        assert r.json['max_rating'] == max(new_ratings)
