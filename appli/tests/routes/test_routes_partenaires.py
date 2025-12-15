def test_partenaires(client):
    response = client.get('/partenaires/', follow_redirects=True)
    assert b"Partenaires" in response.data