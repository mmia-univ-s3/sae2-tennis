def login(client, next):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": next
    }, follow_redirects=True)
    
def test_forms_partenaires_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/partenaires/5/delete/")
        response = client.post('/partenaires/5/delete/', follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/partenaires/" in response.request.path
        assert b"Part5" not in response.data