def test_login(client, testapp):
    with testapp.app_context():
        response = client.post('/connexion/', data={
            "login": "michel",
            "password": "1"
        }, follow_redirects=True)
        assert response.status_code == 200
        assert f"/" in response.request.path
        
def test_login_bad_password(client, testapp):
    with testapp.app_context():
        response = client.post('/connexion/', data={
            "login": "michel",
            "password": "2"
        }, follow_redirects=True)
        assert response.status_code == 200
        assert f"/connexion/" in response.request.path

def test_login_bad_login(client, testapp):
    with testapp.app_context():
        response = client.post('/connexion/', data={
            "login": "michal",
            "password": "1"
        }, follow_redirects=True)
        assert response.status_code == 200
        assert f"/connexion/" in response.request.path