import json
import pytest
from server import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def clubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

@pytest.fixture(scope='module')
def competitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions

def test_get_home_page(client):
    res = client.get('/')

    assert res.status_code == 200
    assert b'<form action="showSummary"' in res.data
    assert b'<input' in res.data

def test_post_summary_page(client, clubs, competitions):
    res = client.post('/showSummary',
        data=dict(email=clubs[0]['email']),
        follow_redirects=True)

    assert res.status_code == 200
    assert b'<h3>Competitions:</h3>'

    for competition in competitions:
        assert str.encode(competition['name']) in res.data
        assert str.encode(competition['date']) in res.data
        assert str.encode(competition['numberOfPlaces']) in res.data
