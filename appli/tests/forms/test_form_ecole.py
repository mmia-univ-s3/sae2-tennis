# pylint: disable=duplicate-code
def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)

def test_forms_ecole(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/ecole-de-tennis/")
        response = client.post('/formation/ecole-de-tennis/', data={
            "editor": "Ecole de tennis 1"
        }, follow_redirects=True)

        assert response.status_code == 200
        assert "/formation/ecole-de-tennis/" in response.request.path
        assert b"Ecole de tennis 1" in response.data
