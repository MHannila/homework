import bson
from bson.errors import InvalidId
from flask import Flask, jsonify, request
from marshmallow import ValidationError
from pymongo.errors import OperationFailure
from werkzeug.exceptions import NotFound

from models import Rating, Song

app = Flask(__name__)


@app.errorhandler(ValidationError)
def handle_schema_validation_error(e):
    response = jsonify(dict(errors=e.messages))
    response.status_code = 400
    return response


@app.route('/songs', methods=['GET'])
def songs():
    try:
        limit = int(request.args['limit'])  # TODO: deserialise with marshmallow
    except:
        limit = None
    try:
        start_from = int(request.args['start_from'])  # TODO: deserialise with marshmallow
    except KeyError:
        start_from = None
    response = dict(
        results=Song.Schemas.Get(many=True).dump(Song.get_all(start_from=start_from, limit=limit)),
    )
    if limit and len(response['results']) == limit:
        response['next_start'] = limit + start_from if start_from else limit

    return jsonify(response)


@app.route('/songs/avg/difficulty', methods=['GET'])
def songs_avg_difficulty():
    id = 'all songs'
    pipelines = []
    try:
        level = request.args['level']
        pipelines.append({
            '$match': {
                'level': int(level),  # TODO: deserialise all inputs so there's no need to cast to int here
            }
        })
        id = f'level {level} songs'
    except KeyError:  # No level
        pass

    pipelines.append({
        '$group': {
            '_id': id,
            'average_difficulty': {'$avg': '$difficulty'},
        },
    })
    try:
        result = next(Song.collection().aggregate(pipeline=pipelines))
    except StopIteration:
        result = dict(
            _id='Database is empty',
            average_difficulty=None,
        )
    return jsonify(result)


@app.route('/songs/search', methods=['GET'])
def songs_search():
    try:
        message = request.args['message']
    except KeyError:
        message = ''

    try:
        # TODO: if/when partial matches are required and/or performance becomes an issue, refactor to use elasticsearch
        result = list(Song.collection().aggregate(
            pipeline=[{
                '$match': {
                    '$text': {'$search': message},
                },
            }]
        ))
        results = Song.Schemas.Get(many=True).dump(result)
    except OperationFailure as e:
        if "no such collection 'homework.songs'" not in e._message:
            raise e
        results = []
    return jsonify(dict(
        results=results,
    ))


@app.route('/songs/rating', methods=['POST'])
def songs_new_rating():
    validated_data = Rating.Schemas.Post().load(request.json)
    Rating.insert(validated_data)  # `validated_data` gets updated to include `_id`
    return jsonify(Rating.Schemas.Get().dump(validated_data))


@app.route('/songs/avg/rating/<string:song_id>', methods=['GET'])  # TODO: convert id to ObjectId automatically
def songs_avg_rating(song_id):
    try:
        song_id = bson.ObjectId(song_id)
    except InvalidId:
        raise NotFound  # TODO: should return this also when valid ObjectId, but song with the id doesn't exist
    try:
        result = next(Rating.collection().aggregate(
            pipeline=[
                {'$match': {
                    'song_id': bson.ObjectId(song_id)},
                },
                {
                    '$group': {
                        '_id': '$song_id',
                        'average_rating': {'$avg': '$rating'},
                        'min_rating': {'$min': '$rating'},
                        'max_rating': {'$max': '$rating'},
                    },
                },
            ]
        ))
        del result['_id']
    except StopIteration:
        result = dict(
            average_rating=None,
            min_rating=None,
            max_rating=None,
        )
    return jsonify(result)


######################################################################################################################
# Below some endpoints for generating random data and resetting the database to see how it affects the above endpoints
######################################################################################################################

@app.route('/add_random_song', methods=['GET'])
def add_random_song():
    import random
    from faker import Faker

    fake = Faker()
    insert_data = dict(
        artist=' '.join(fake.words(nb=4)),
        title=' '.join(fake.words(nb=4)),
        difficulty=random.uniform(1, 20),
        level=random.randint(1, 15),
        released=str(fake.date()),
    )
    Song.insert(insert_data)
    return jsonify(Song.Schemas.Get().dump(insert_data))


@app.route('/add_random_rating', methods=['GET'])
def add_random_rating():
    import random
    insert_data = dict(
        song_id=random.choice(list(Song.get_all()))['_id'],
        rating=random.randint(1, 5)
    )
    Rating.insert(insert_data)
    return jsonify(Rating.Schemas.Get().dump(insert_data))


@app.route('/recreate_database', methods=['GET'])
def reset_db():
    from tools.setup_db import recreate_database
    recreate_database()
    return ('', 204)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
