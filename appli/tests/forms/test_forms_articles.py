# pylint: disable=missing-function-docstring

# pylint: disable=duplicate-code
def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)

def test_article_create(client, testapp):
    with testapp.app_context():
        response = login(client, "/club/articles/create/")
        response = client.post('/club/articles/create/', data={
            "titre": "article89",
            "editor":"blabla",
            "type_a":"club"
        }, follow_redirects=True)

        assert response.status_code == 200
        assert "/club/articles/" in response.request.path
        assert b"blabla" in response.data

def test_article_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/club/articles/21/delete/")
        response = client.post('/club/articles/21/delete/', follow_redirects=True)

        assert response.status_code == 200
        assert "/club/articles/" in response.request.path
        assert b"blabla" not in response.data

def test_article_maj(client, testapp):
    with testapp.app_context():
        response = login(client, "/club/articles/2/")
        response = client.post('/club/articles/2/', follow_redirects=True)
        response = client.post('/club/articles/2/', data={
            "titre": "Stephane a perdu",
            "editor":"blabla",
            "type_a":"club"
        }, follow_redirects=True)

        assert response.status_code == 200
        assert "/club/articles/" in response.request.path
        assert b"blabla" in response.data
