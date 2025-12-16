# pylint: disable=missing-function-docstring

# pylint: disable=duplicate-code
def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)

def test_forms_logout(client):
    response = client.post("/deconnexion/", follow_redirects=True)
    assert response.status_code == 200
    assert "/" in response.request.path
