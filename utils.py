import json

def load_clubs():
    clubs_file = open('clubs.json')
    clubs_values = json.load(clubs_file)['clubs']
    clubs_file.close()

    return clubs_values

def load_competitions():
    competitions_file = open('competitions.json')
    competitions_values = json.load(competitions_file)['competitions']
    competitions_file.close()

    return competitions_values

def find_by(key, value, items):
    item = (item for item in items if item[key] == value)
    return next(item, False)

def update_club_from_slug(slug, payload):
    clubs = load_clubs()
    filtred_clubs = [club for club in clubs if club['slug'] != slug]

    clubs_file = open('clubs.json', 'w')
    json.dump({
        "clubs": [*filtred_clubs, payload]
    }, clubs_file, indent=4)
    clubs_file.close()

def update_competition_from_slug(slug, payload):
    competitions = load_competitions()
    filtred_competitions = [competition for competition in competitions if competition['slug'] != slug]

    competitions_file = open('competitions.json', 'w')
    json.dump({
        "competitions": [*filtred_competitions, payload]
    }, competitions_file, indent=4)
    competitions_file.close()

def reset_jsons():
    clubs = {'clubs': [{'name': 'She Lifts', 'slug': 'she-lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}, {'name': 'Iron Temple', 'slug': 'iron-temple', 'email': 'admin@irontemple.com', 'points': '4'}, {'name': 'Simply Lift', 'slug': 'simply-lift', 'email': 'john@simplylift.co', 'points': '675'}]}
    competitions = {'competitions': [{'name': 'Fall Classic', 'slug': 'fall-classic', 'date': '2020-10-22 13:30:00', 'numberOfPlaces': '8'}, {'name': 'Spring Festival', 'slug': 'spring-festival', 'date': '2020-03-27 10:00:00', 'numberOfPlaces': '13'}]}

    competitions_file = open('competitions.json', 'w')
    json.dump(competitions, competitions_file, indent=4)
    competitions_file.close()

    clubs_file = open('clubs.json', 'w')
    json.dump(clubs, clubs_file, indent=4)
    clubs_file.close()
