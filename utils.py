import json

def find_from_slug(items, slug):
    item = (item for item in items if item['slug'] == slug)
    return next(item, False)

def find_by(key, value, items):
    item = (item for item in items if item[key] == value)
    return next(item, False)

def load_clubs():
    with open('clubs.json') as club:
        return json.load(club)['clubs']

def load_competitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']

def update_club_from_slug(slug, payload):
    clubs = load_clubs()
    filtred_clubs = [club for club in clubs if club['slug'] != slug]

    with open('clubs.json', 'w') as file:
        json.dump({
            "clubs": [*filtred_clubs, payload]
        }, file, indent=4)

def update_competition_from_slug(slug, payload):
    competitions = load_competitions()
    filtred_competitions = [competition for competition in competitions if competition['slug'] != slug]

    with open('competitions.json', 'w') as file:
        json.dump({
            "competitions": [*filtred_competitions, payload]
        }, file, indent=4)

def reset_jsons():
    clubs = {'clubs': [{'name': 'She Lifts', 'slug': 'she-lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}, {'name': 'Iron Temple', 'slug': 'iron-temple', 'email': 'admin@irontemple.com', 'points': '4'}, {'name': 'Simply Lift', 'slug': 'simply-lift', 'email': 'john@simplylift.co', 'points': '675'}]}
    competitions = {'competitions': [{'name': 'Fall Classic', 'slug': 'fall-classic', 'date': '2020-10-22 13:30:00', 'numberOfPlaces': '8'}, {'name': 'Spring Festival', 'slug': 'spring-festival', 'date': '2020-03-27 10:00:00', 'numberOfPlaces': '13'}]}

    with open('competitions.json', 'w') as file:
        json.dump(competitions, file, indent=4)

    with open('clubs.json', 'w') as file:
        json.dump(clubs, file, indent=4)
