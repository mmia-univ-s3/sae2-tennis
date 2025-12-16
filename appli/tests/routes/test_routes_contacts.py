def test_contacts(client):
    response = client.get('/contacts/', follow_redirects=True)
    assert b"Contacts" in response.data
