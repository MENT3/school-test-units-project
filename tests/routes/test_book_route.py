import random
import pytest
from random import choice

def test_get_book_success(client, competitions):
    competition = competitions[0]
    club_slug = 'simply-lift'

    with client.session_transaction() as sess:
        sess['club_slug'] = club_slug

    res = client \
            .get('/book/{competition_slug}/{club_slug}' \
            .format(competition_slug=competition['slug'], club_slug=club_slug))

    assert res.status_code == 200

    html = res.data.decode()
    assert '<h1 class="text-xl text-gray-800 font-bold">\n  {competition_name}\n</h1>' \
        .format(competition_name=competition['name']) in html

    assert competition['numberOfPlaces'] in html

@pytest.mark.parametrize('competition_slug, club_slug', [
  ('invalid', 'simply-lift'),
  ('spring-festival', 'invalid'),
  ('invalid', 'invalid')
])

def test_get_book_with_invalid_slug(client, competition_slug, club_slug):
    with client.session_transaction() as sess:
        sess['club_slug'] = club_slug

    res = client.get('/book/{competition_slug}/{club_slug}' \
            .format(competition_slug=competition_slug, club_slug=club_slug))

    assert res.status_code == 404
    assert 'Something went wrong-please try again' in res.data.decode()

def test_post_when_not_logged_in(client, competitions):
    competition = competitions[0]

    res = client \
            .get('/book/{competition_slug}/simply-lift' \
            .format(competition_slug=competition['slug']))

    assert res.status_code == 403

def test_post_when_logged_in_but_unauthorized(client, clubs, competitions):
    competition = competitions[0]

    random_club = choice(clubs)
    another_random_club = choice([club for club in clubs \
        if club['slug'] != random_club['slug']])

    with client.session_transaction() as sess:
        sess['club_slug'] = random_club['slug']

    res = client.get('/book/{competition_slug}/{club_slug}' \
                .format(competition_slug=competition['slug'],
                        club_slug=another_random_club['slug']))

    assert res.status_code == 403
