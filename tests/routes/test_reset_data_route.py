from random import choice
from utils import find_by, load_clubs, load_competitions, update_club_from_slug, update_competition_from_slug

def test_get_data_reset_success(client, clubs, competitions):
    random_club = choice(clubs)
    random_competition = choice(competitions)

    update_club_from_slug(random_club['slug'], {
        **random_club,
        'name': 'updated'
    })

    update_competition_from_slug(random_competition['slug'], {
        **random_competition,
        'name': 'updated'
    })

    clubs = load_clubs()
    competitions = load_competitions()

    finded_club = find_by('slug', random_club['slug'], clubs)
    finded_competition = find_by('slug', random_competition['slug'], competitions)

    assert finded_club['name'] == 'updated'
    assert finded_competition['name'] == 'updated'

    res = client.get('/reset-data')
    assert res.status_code == 302

    clubs = load_clubs()
    competitions = load_competitions()

    finded_club = find_by('slug', random_club['slug'], clubs)
    finded_competition = find_by('slug', random_competition['slug'], competitions)

    assert finded_club['name'] == random_club['name']
    assert finded_competition['name'] == random_competition['name']
