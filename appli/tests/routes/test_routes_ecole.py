# pylint: disable=missing-function-docstring

def test_ecole(client):
    response = client.get('/formation/ecole-de-tennis/', follow_redirects=True)
    assert b"Ecole de tennis 1" in response.data
