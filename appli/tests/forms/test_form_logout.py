def login(client, next):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": next
    }, follow_redirects=True)
    
def test_forms_logout(client):
    response = client.post("/deconnexion/", follow_redirects=True)
    assert response.status_code == 200
    assert f"/" in response.request.path