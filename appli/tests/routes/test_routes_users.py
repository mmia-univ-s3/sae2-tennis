# pylint: disable=missing-function-docstring

def test_users(client):
    response = client.get('/connexion/', follow_redirects=True)
    assert b"Se connecter" in response.data
