# pylint: disable=missing-function-docstring

def test_index(client):
    response = client.get('/', follow_redirects=True)
    assert b"/static/banner.png" in response.data
    assert b"art7" in response.data
    #assert b"Halo" in response.data
    assert b"Futurs championnats" in response.data
    assert b"championnat equipe 1" in response.data
