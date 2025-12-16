# pylint: disable=duplicate-code
def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)

def test_forms_management(client, testapp):
    with testapp.app_context():
        response = login(client, "/club/management/")
        response = client.post('/club/management/', data={
            "editor": "blabla"
        }, follow_redirects=True)

        assert response.status_code == 200
        assert "/club/management/" in response.request.path
        assert b"blabla" in response.data
