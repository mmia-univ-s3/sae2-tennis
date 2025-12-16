# pylint: disable=duplicate-code
def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)

def test_forms_documents(client, testapp):
    with testapp.app_context():
        response = login(client, "/club/documents/")
        response = client.post('/club/documents/', data={
            "editor": "Document 1"
        }, follow_redirects=True)

        assert response.status_code == 200
        assert "/club/documents/" in response.request.path
        assert b"Document 1" in response.data
