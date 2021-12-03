import pytest
from utils import find_from_slug, load_clubs, load_competitions

def test_post_success(client, reset_data, clubs, competitions):
    reset_data

    competition = find_from_slug(competitions, 'spring-festival')
    club = find_from_slug(clubs, 'simply-lift')

    number_of_places_before_request = competition['numberOfPlaces']
    club_points_before_request = club['points']

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

    competition = find_from_slug(competitions, 'spring-festival')
    club = find_from_slug(clubs, 'simply-lift')

    assert int(competition['numberOfPlaces']) == int(number_of_places_before_request) - 1
    assert int(club['points']) == int(club_points_before_request) - 5

@pytest.mark.parametrize('club_slug, competition_slug, requested_places', [
    ('simply-lift', 'spring-festival', 13)
])
def test_post_when_invalid(client, reset_data, clubs, competitions, club_slug, competition_slug, requested_places):
    reset_data

    club = find_from_slug(clubs, club_slug)
    competition = find_from_slug(competitions, competition_slug)

    number_of_places_before_request = competition['numberOfPlaces']
    club_points_before_request = club['points']

    res = client.post('/purchasePlaces', data=dict(
        club=club['slug'],
        competition=competition['slug'],
        places=requested_places
    ))

    assert res.status_code == 500
    assert 'Impossible de réserver' in res.data.decode()

    # Reload data
    competitions = load_competitions()
    clubs = load_clubs()

    club = find_from_slug(clubs, club_slug)
    competition = find_from_slug(competitions, competition_slug)

    assert int(competition['numberOfPlaces']) == int(number_of_places_before_request)
    assert int(club['points']) == int(club_points_before_request)
