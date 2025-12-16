# pylint: disable=missing-function-docstring

# pylint: disable=duplicate-code
def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)

def test_forms_histoire_texte(client, testapp):
    with testapp.app_context():
        response = login(client, "/club/histoire/")
        response = client.post('/club/histoire/', data={
            "editor": "2020 : confinement"
        }, follow_redirects=True)

        assert response.status_code == 200
        assert "/club/histoire/" in response.request.path
        assert b"2020 : confinement" in response.data

def test_forms_histoire_information(client, testapp):
    with testapp.app_context():
        response = login(client, "/club/histoire/ajout/")
        response = client.post('/club/histoire/ajout/', data={
            "annee": "2012",
            "trivia": "fin du monde"
        }, follow_redirects=True)

        assert response.status_code == 200
        assert "/club/histoire/" in response.request.path
        assert b"fin du monde" in response.data

def test_forms_histoire_information_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/club/histoire/2/delete/")
        response = client.post('/club/histoire/2/delete/', follow_redirects=True)

        assert response.status_code == 200
        assert "/club/histoire/" in response.request.path
        assert b"texte2" not in response.data
