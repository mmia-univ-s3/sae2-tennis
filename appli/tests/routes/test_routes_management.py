# pylint: disable=missing-function-docstring

def test_management(client):
    response = client.get('/club/management/', follow_redirects=True)
    assert b"Management du club" in response.data
    assert b"banane" in response.data
