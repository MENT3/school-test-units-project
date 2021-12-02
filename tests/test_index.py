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

def test_home_page(client):
    res = client.get('/')

    assert res.status_code == 200
    assert b'<form action="showSummary"' in res.data
    assert b'<input' in res.data

def test_summary_page(client, clubs):
    res = client.post('/showSummary',
        data=dict(email=clubs[0]['email']),
        follow_redirects=True)

    print(res.status_code)
    print(res.data.decode())
