# pylint: disable=duplicate-code
def login(client, next):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": next
    }, follow_redirects=True)

def test_partenaires(client):
    response = client.get('/partenaires/', follow_redirects=True)
    assert b"Partenaires" in response.data
    
def test_partenaires_delete_confirm(client, testapp):
    with testapp.app_context():
        response = login(client, "/partenaire/1/delete/")
        response = client.get('/partenaire/1/delete/', follow_redirects=True)
        assert b"Suppression d'un partenaire" in response.data