import random

def test_first_scenario(client, reset_data, clubs, competitions):
    reset_data

    # index
    index_res = client.get('/', follow_redirects=True)

    assert index_res.status_code == 200

    # show summary
    random_club = random.choice(clubs)
    show_summary_res = client.post('/showSummary', data=dict(
        email=random_club['email']
    ), follow_redirects=True)

    assert show_summary_res.status_code == 200

    with client.session_transaction() as sess:
        assert 'club_slug' in sess
        assert sess['club_slug'] == random_club['slug']

    # book
    random_competition = random.choice(competitions)
    book_url = 'book/{competition_slug}/{club_slug}' \
        .format(competition_slug=random_competition['slug'],
                club_slug=random_club['slug'])

    book_res = client.get(book_url, follow_redirects=True)

    assert book_res.status_code == 200

    # purchase places
    purchase_places_res = client.post('/purchasePlaces', data=dict(
        club=random_club['slug'],
        competition=random_competition['slug'],
        places=1
    ), follow_redirects=True)

    assert purchase_places_res.status_code == 200

    # logout
    logout_res = client.get('/logout', follow_redirects=True)

    assert logout_res.status_code == 200

    with client.session_transaction() as sess:
        assert 'club_slug' not in sess
