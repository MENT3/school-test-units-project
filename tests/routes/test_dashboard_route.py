def test_get_dashboard_success(client, reset_data, clubs, competitions):
    res = client.get('/dashboard')

    assert res.status_code == 200

    html = res.data.decode()
    for club in clubs:
        for v in club.values():
            assert v in html

    for competition in competitions:
        for v in competition.values():
            assert v in html
