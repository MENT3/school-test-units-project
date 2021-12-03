import json
import pytest
from server import app as flask_app

from utils import loadClubs, loadCompetitions

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def clubs():
    return loadClubs()

@pytest.fixture(scope='module')
def competitions():
    return loadCompetitions()
