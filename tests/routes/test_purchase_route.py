import pytest
from utils import find_by, load_clubs, load_competitions

def test_post_success(client, reset_data, clubs, competitions):
    reset_data

    competition = find_by('slug', 'spring-festival', competitions)
    club = find_by('slug', 'simply-lift', clubs)

    number_of_places_before_request = competition['numberOfPlaces']
    club_points_before_request = club['points']

    with client.session_transaction() as sess:
        sess['club_slug'] = club['slug']

    res = client.post('/purchasePlaces', data=dict(
        club=club['slug'],
        competition=competition['slug'],
        places=1
    ))

    assert res.status_code == 200
    assert 'Great-booking complete!' in res.data.decode()

    # Reload data
    competitions = load_competitions()
    clubs = load_clubs()

    competition = find_by('slug', 'spring-festival', competitions)
    club = find_by('slug', 'simply-lift', clubs)

    assert int(competition['numberOfPlaces']) == int(number_of_places_before_request) - 1
    assert int(club['points']) == int(club_points_before_request) - 3

@pytest.mark.parametrize('club_slug, competition_slug, requested_places', [
    ('simply-lift', 'spring-festival', 13), # Test more than 12 place requested
    ('iron-temple', 'spring-festival', 10), # Test club insuffisant points
    ('simply-lift', 'fall-classic', 10) # Test competition insuffisant remeaning places
])
def test_post_when_invalid(client, reset_data, clubs, competitions, club_slug, competition_slug, requested_places):
    reset_data

    club = find_by('slug', club_slug, clubs)
    competition = find_by('slug', competition_slug, competitions)

    club_points_before_request = club['points']
    number_of_places_before_request = competition['numberOfPlaces']

    with client.session_transaction() as sess:
        sess['club_slug'] = club['slug']

    res = client.post('/purchasePlaces', data=dict(
        club=club['slug'],
        competition=competition['slug'],
        places=requested_places
    ), follow_redirects=True)

    assert res.status_code == 500
    assert 'Impossible de r??server' in res.data.decode()

    # Reload data
    competitions = load_competitions()
    clubs = load_clubs()

    club = find_by('slug', club_slug, clubs)
    competition = find_by('slug', competition_slug, competitions)

    assert int(club['points']) == int(club_points_before_request)
    assert int(competition['numberOfPlaces']) == int(number_of_places_before_request)

def test_post_when_not_logged_in(client):
    res = client.post('/purchasePlaces', data=dict(
        club='simply-lift',
        competition='fall-classic',
        places=1
    ), follow_redirects=True)

    assert res.status_code == 403
