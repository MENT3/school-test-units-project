import pytest

def test_get_book_success(client, competitions):
  competition = competitions[0]
  res = client \
    .get('/book/{competition_slug}/simply-lift' \
    .format(competition_slug=competition['slug']))

  assert res.status_code == 200

  html = res.data.decode()
  assert '<h2>{competition_name}</h2>'.format(competition_name=competition['name']) in html
  assert competition['numberOfPlaces'] in html

@pytest.mark.parametrize('invalid_uri', [
  '/book/invalid/simply-lift',
  '/book/spring-festival/invalid',
  '/book/invalid/invalid'
])
def test_get_book_with_invalid_slug(client, invalid_uri):
  res = client.get(invalid_uri)

  assert res.status_code == 404
  assert 'Something went wrong-please try again' in res.data.decode()
