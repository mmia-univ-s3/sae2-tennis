# pylint: disable=missing-function-docstring

def test_redirect_club(client):
    response = client.get('/club/', follow_redirects=True)
    assert "/club/histoire/" in response.request.url

def test_redirect_competitions(client):
    response = client.get('/competitions/', follow_redirects=True)
    assert "/competitions/calendrier/" in response.request.url

def test_redirect_formation(client):
    response = client.get('/formation/', follow_redirects=True)
    assert "/formation/tarifications/" in response.request.url
