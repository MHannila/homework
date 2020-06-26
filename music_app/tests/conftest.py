import pytest


@pytest.fixture
def client():
    from music_app.src.api import app
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client
