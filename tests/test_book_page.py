def test_get_book_success(client, competitions):
  competition = competitions[0]
  res = client \
    .get('/book/{competition_slug}/simply-lift' \
    .format(competition_slug=competition['slug']))

  assert res.status_code == 200

  html = res.data.decode()
  assert '<h2>{competition_name}</h2>'.format(competition_name=competition['name']) in html
  assert competition['numberOfPlaces'] in html
