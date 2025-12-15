def test_tarifications(client):
    response = client.get('/formation/tarifications/', follow_redirects=True)
    assert b"230.00" in response.data