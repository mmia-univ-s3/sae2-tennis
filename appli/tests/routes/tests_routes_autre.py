def test_autres(client):
    response = client.get('/club/autres-sports/', follow_redirects=True)
    assert b"Autres sports sur le stade" in response.data