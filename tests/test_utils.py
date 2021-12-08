import json
from random import choice
from utils import find_by, load_competitions, load_clubs, reset_jsons, update_club_from_slug, update_competition_from_slug

def test_load_competitions():
    json_file = open('competitions.json')
    values = json.load(json_file)['competitions']
    json_file.close()

    assert load_competitions() == values

def test_load_clubs():
    json_file = open('clubs.json')
    values = json.load(json_file)['clubs']
    json_file.close()

    assert load_clubs() == values

def test_find_from(clubs):
    finded_club = find_by('slug', clubs[0]['slug'], clubs)

    assert finded_club == clubs[0]

def test_update_club_from_slug(reset_data, clubs):
    random_club = choice(clubs)
    payload = { **random_club,
        'email': 'updated@email.com',
        'points': '999'
    }

    filtred_clubs = [club for club in clubs if club['slug'] != random_club['slug']]
    update_club_from_slug(random_club['slug'], payload)

    calculated_values = [
        *filtred_clubs,
        payload
    ]
    calculated_values = sorted(calculated_values, key=lambda club: club['slug'])

    updated_clubs = load_clubs()
    updated_clubs = sorted(updated_clubs, key=lambda club: club['slug'])


    assert updated_clubs == calculated_values

def test_update_competition_from_slug(reset_data, competitions):
    random_competition = choice(competitions)
    payload = {
        **random_competition,
        'name': 'Updated name',
        'numberOfPlaces': '999'
    }

    filtred_clubs = [
        competition for competition in competitions \
            if competition['slug'] != random_competition['slug']
    ]

    update_competition_from_slug(random_competition['slug'], payload)

    calculated_values = [
        *filtred_clubs,
        payload
    ]
    calculated_values = sorted(calculated_values, key=lambda club: club['slug'])

    updated_clubs = load_competitions()
    updated_clubs = sorted(updated_clubs, key=lambda club: club['slug'])

    assert updated_clubs == calculated_values

def test_reset_json():
    clubs = [{'name': 'She Lifts', 'slug': 'she-lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}, {'name': 'Iron Temple', 'slug': 'iron-temple', 'email': 'admin@irontemple.com', 'points': '4'}, {'name': 'Simply Lift', 'slug': 'simply-lift', 'email': 'john@simplylift.co', 'points': '675'}]
    competitions = [{'name': 'Fall Classic', 'slug': 'fall-classic', 'date': '2020-10-22 13:30:00', 'numberOfPlaces': '8'}, {'name': 'Spring Festival', 'slug': 'spring-festival', 'date': '2020-03-27 10:00:00', 'numberOfPlaces': '13'}]

    reset_jsons()

    assert competitions == load_competitions()
    assert clubs == load_clubs()
