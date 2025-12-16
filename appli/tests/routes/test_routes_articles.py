# pylint: disable=duplicate-code
def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)

def test_articles(client):
    response = client.get('/club/articles/', follow_redirects=True)
    assert b"Articles du club" in response.data

def test_article_view(client):
    response = client.get('/club/articles/2/', follow_redirects=True)
    assert b"Hi" in response.data

def test_article_delete_confirm(client, testapp):
    with testapp.app_context():
        response = login(client, "/club/articles/2/delete/")
        response = client.get('/club/articles/2/delete/', follow_redirects=True)
        assert b"Suppression d'un article" in response.data
