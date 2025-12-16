from appli.models.article import Article
from appli.app import db

# pylint: disable=duplicate-code
def login(client, next):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": next
    }, follow_redirects=True)
    
def test_forms_contacts_modif_adresse(client, testapp):
    with testapp.app_context():
        response = login(client, "/contacts/adresse/")
        response = client.post('/contacts/adresse/', data={
            "editor": "123 Rue du Test, 75001 Paris, France"
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/contacts/" in response.request.path
        assert b"123 Rue du Test, 75001 Paris, France" in response.data
        
def test_forms_contacts_modif_telephone(client, testapp):
    with testapp.app_context():
        response = login(client, "/contacts/telephone/")
        response = client.post('/contacts/telephone/', data={
            "editor": "06 06 06 06 06"
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/contacts/" in response.request.path
        assert b"06 06 06 06 06" in response.data
        
def test_forms_contacts_modif_mail(client, testapp):
    with testapp.app_context():
        response = login(client, "/contacts/email/")
        response = client.post('/contacts/email/', data={
            "editor": "stade@tennis.com"
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/contacts/" in response.request.path
        assert b"stade@tennis.com" in response.data
        
def test_forms_contacts_create_adresse(client, testapp):
    with testapp.app_context():
        page = Article.query.filter(Article.titre == "_adresse" and Article.type_article == "pages").first() 
        db.session.delete(page)
        db.session.commit()
        response = login(client, "/contacts/adresse/")
        response = client.post('/contacts/adresse/', data={
            "editor": "123 Rue du Test, 75001 Paris, France"
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/contacts/" in response.request.path
        assert b"123 Rue du Test, 75001 Paris, France" in response.data
        
def test_forms_contacts_create_telephone(client, testapp):
    with testapp.app_context():
        page = Article.query.filter(Article.titre == "_tel" and Article.type_article == "pages").first() 
        db.session.delete(page)
        db.session.commit()
        response = login(client, "/contacts/telephone/")
        response = client.post('/contacts/telephone/', data={
            "editor": "06 06 06 06 06"
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/contacts/" in response.request.path
        assert b"06 06 06 06 06" in response.data
        
def test_forms_contacts_create_mail(client, testapp):
    with testapp.app_context():
        page = Article.query.filter(Article.titre == "_mail" and Article.type_article == "pages").first() 
        db.session.delete(page)
        db.session.commit()
        response = login(client, "/contacts/email/")
        response = client.post('/contacts/email/', data={
            "editor": "stade@tennis.com"
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/contacts/" in response.request.path
        assert b"stade@tennis.com" in response.data