def test_ecole(client):
    response = client.get('/formation/ecole-de-tennis/', follow_redirects=True)
    assert b"cole de Tennis" in response.data