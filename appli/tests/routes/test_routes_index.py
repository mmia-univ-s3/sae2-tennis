def test_index(client):
    response = client.get('/', follow_redirects=True)
    assert b"News du Stade Poitevin Tennis" in response.data
