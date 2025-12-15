def test_articles(client):
    response = client.get('/club/articles/', follow_redirects=True)
    assert b"Articles du club" in response.data
    
def test_article_view(client):
    response = client.get('/club/articles/2/', follow_redirects=True)
    assert b"Hi" in response.data