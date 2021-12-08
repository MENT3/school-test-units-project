def test_post_summary_success(client, clubs, competitions):
    res = client.post('/showSummary',
        data=dict(email=clubs[0]['email']),
        follow_redirects=True)

    assert res.status_code == 200
    assert b'<h3>Competitions:</h3>'

    for competition in competitions:
        assert str.encode(competition['name']) in res.data
        assert str.encode(competition['date']) in res.data
        assert str.encode(competition['numberOfPlaces']) in res.data

def test_post_summary_invalid_email(client):
    res = client.post('/showSummary',
        data=dict(email='invalid@email.com'),
        follow_redirects=True)

    assert res.status_code == 404
    assert 'Désolé, cet email n&#39;a pas été trouvé' in res.data.decode()
