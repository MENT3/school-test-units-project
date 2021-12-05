def test_get_home_success(client):
    res = client.get('/')

    assert res.status_code == 200
    assert b'<form\n        action="showSummary"' in res.data
    assert b'<input' in res.data
