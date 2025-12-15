def test_documents(client):
    response = client.get('/club/documents/', follow_redirects=True)
    assert b"Documents administratifs" in response.data