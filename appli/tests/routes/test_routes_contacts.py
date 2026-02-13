# pylint: disable=missing-function-docstring

def test_contacts(client):
    response = client.get('/contacts/', follow_redirects=True)
    assert b"123 Rue du Test, 75001 Paris" in response.data
    assert b"06 06 06 06 06" in response.data
    assert b"stade@tennis.com" in response.data
    assert b"Facebook" in response.data
