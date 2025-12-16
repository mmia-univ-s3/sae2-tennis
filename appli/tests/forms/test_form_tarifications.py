# pylint: disable=duplicate-code
def login(client, next):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": next
    }, follow_redirects=True)
    
def test_forms_categorie(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/tarifications/ajout/categorie/")
        response = client.post('/formation/tarifications/ajout/categorie/', data={
            "intitule":"cate1",
            "sport":"tennis"
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/formation/tarifications/" in response.request.path
        assert b"cate1" in response.data
        
def test_forms_categorie_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/tarifications/categorie/2/delete/")
        response = client.post('/formation/tarifications/categorie/2/delete/', follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/formation/tarifications/" in response.request.path
        assert b"sion adulte" not in response.data
        assert b"entre 1997 et 2007" not in response.data

def test_forms_sous_categorie_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/tarifications/categorie/12/delete/")
        response = client.post('/formation/tarifications/categorie/12/delete/', follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/formation/tarifications/" in response.request.path
        assert b"servation des cours 9h/semaine" not in response.data
        
def test_forms_sous_categorie(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/tarifications/categorie/4/souscategorie/")
        response = client.post('/formation/tarifications/categorie/4/souscategorie/', data={
            "intitule":"sous-cate1", "sport": "tennis"}
            , follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/formation/tarifications/" in response.request.path
        assert b"sous-cate1" in response.data
        
def test_forms_reservation(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/tarifications/categorie/6/ajout/reservation/")
        response = client.post('/formation/tarifications/categorie/6/ajout/reservation/', data={
            "intitule":"rese1",
            "montant":"150.00"
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/formation/tarifications/" in response.request.path
        assert b"rese1" in response.data
        
def test_forms_reduction(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/tarifications/categorie/6/ajout/reduction/")
        response = client.post('/formation/tarifications/categorie/6/ajout/reduction/', data={
            "intitule":"redu1",
            "taux":"50%",
            "cumulable":"true"
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/formation/tarifications/" in response.request.path
        assert b"redu1" in response.data
        
def test_forms_reservation_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/tarifications/tarif/6/update-reservation/")
        response = client.post('/formation/tarifications/tarif/6/update-reservation/', data={
            "intitule":"rese1",
            "montant":"160.00"
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/formation/tarifications/" in response.request.path
        assert b"160.00" in response.data
        
def test_forms_reduction_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/tarifications/tarif/30/update-reduction/")
        response = client.post('/formation/tarifications/tarif/30/update-reduction/', data={
            "intitule":"redu1",
            "taux":"60%",
            "cumulable":"true"
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/formation/tarifications/" in response.request.path
        assert b"60%" in response.data
        
def test_forms_tarif_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/tarifications/tarif/47/delete/")
        response = client.post('/formation/tarifications/tarif/47/delete/', follow_redirects=True)
        
        assert response.status_code == 200
        assert f"/formation/tarifications/" in response.request.path
        assert b"Tube de 3 balles" not in response.data