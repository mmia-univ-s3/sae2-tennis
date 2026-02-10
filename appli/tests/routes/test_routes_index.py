# pylint: disable=missing-function-docstring

def test_index(client):
    response = client.get('/', follow_redirects=True)
    assert b"/static/banner.png" in response.data
