# pylint: disable=duplicate-code
def login(client, next):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": next
    }, follow_redirects=True)
    
def test_forms_documents(client, testapp):
    with testapp.app_context():
        response = login(client, "/club/documents/")
        response = client.post('/club/documents/', data={
            "editor": "Document 1"
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/club/documents/" in response.request.path
        assert b"Document 1" in response.data