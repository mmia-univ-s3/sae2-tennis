# pylint: disable=missing-function-docstring

def test_histoire(client):
    response = client.get('/club/histoire/', follow_redirects=True)
    assert b"Histoire du club" in response.data
