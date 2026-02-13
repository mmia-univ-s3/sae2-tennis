# pylint: disable=missing-function-docstring

def test_histoire(client):
    response = client.get('/club/histoire/', follow_redirects=True)
    assert b"texte10" in response.data
