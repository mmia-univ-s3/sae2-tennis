# pylint: disable=missing-function-docstring

# pylint: disable=duplicate-code
def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)

def test_tarifications(client):
    response = client.get('/formation/tarifications/', follow_redirects=True)
    assert b"230.00" in response.data
    assert b"Abonnement" in response.data
    assert b"Cartes membres" in response.data
    assert b"Classique Jeune" in response.data

def test_reservation_create(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/tarifications/categorie/8/ajout/reservation/")
        response = client.get('/formation/tarifications/categorie/8/ajout/reservation/',
            follow_redirects=True)
        assert b"Ajout d'une r" in response.data
        assert b"servation" in response.data

def test_reduction_create(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/tarifications/categorie/8/ajout/reduction/")
        response = client.get('/formation/tarifications/categorie/8/ajout/reduction/',
            follow_redirects=True)
        assert b"Ajout d'une r" in response.data
        assert b"duction" in response.data

def test_tarif_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/tarifications/tarif/12/delete/")
        response = client.get('/formation/tarifications/tarif/12/delete/', follow_redirects=True)
        assert b"Voulez-vous vraiment supprimer ce tarif" in response.data

def test_tarif_create(client, testapp):
    with testapp.app_context():
        response = login(client, "/formation/tarifications/categorie/8/ajout/")
        response = client.get('/formation/tarifications/categorie/8/ajout/', follow_redirects=True)
        assert b"Ajout d'un tarif" in response.data
