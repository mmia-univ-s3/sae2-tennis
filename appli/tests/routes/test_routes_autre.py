# pylint: disable=missing-function-docstring

def test_autres(client):
    response = client.get('/autre-sports/', follow_redirects=True)
    assert b"Aquaponey" in response.data
