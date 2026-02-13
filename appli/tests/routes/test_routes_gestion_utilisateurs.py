# pylint: disable=missing-function-docstring

# pylint: disable=duplicate-code
def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)
    
def test_gestion_utilisateurs(client, testapp):
    with testapp.app_context():
        response = login(client, "/utilisateurs/")
        response = client.get('/utilisateurs/', follow_redirects=True)
        assert b"Gestion des utilisateurs" in response.data
        assert b"michel" in response.data
        assert b"Ajouter un nouvel utilisateur" in response.data

def test_utilisateurs_delete_confirm(client, testapp):
    with testapp.app_context():
        response = login(client, "/utilisateurs/martin/delete/")
        response = client.get('/utilisateurs/martin/delete/', follow_redirects=True)
        assert b"Supprimer un utilisateur" in response.data
