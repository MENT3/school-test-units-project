import json
import pytest
from server import app as flask_app
from utils import load_clubs, load_competitions, reset_jsons

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def reset_data():
    return reset_jsons()

@pytest.fixture
def clubs():
    return load_clubs()

@pytest.fixture
def competitions():
    return load_competitions()
