# pylint: disable=missing-function-docstring

def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)

def test_calendrier(client):
    response = client.get('/competitions/calendrier/', follow_redirects=True)
    assert b"Calendrier des comp" in response.data
    assert b"titions" in response.data

def test_palmares(client):
    response = client.get('/competitions/palmares/list/', follow_redirects=True)
    assert b"Palmar" in response.data

def test_tournois_internes(client):
    response = client.get('/competitions/tournois-internes/', follow_redirects=True)
    assert b"Tournois internes" in response.data

def test_internes_add(client):
    response = login(client, "/competitions/tournois-internes/add/")
    response = client.get('competitions/tournois-internes/add/', follow_redirects=True)
    assert b"Ajout d'un match en interne" in response.data

def test_internes_update_not_work(client):
    response = login(client, "/competitions/tournois-internes/2/update/")
    response = client.post('competitions/tournois-internes/2/update/', data={
        "date":"2025-12-14",
        "titre":"Test",
        "serie":"test",
        "joueur1":"1",
        "points1": '4',
        'points2': '7',
        'joueur2':'1'
    }, follow_redirects=True)
    assert b"Modification d'un match" in response.data
    assert "/competitions/tournois-internes/2/update/" in response.request.path

def test_internes_update_work(client):
    response = login(client, "/competitions/tournois-internes/2/update/")
    response = client.post('competitions/tournois-internes/2/update/', data={
        "date":"2025-12-14",
        "titre":"Test",
        "serie":"test",
        "joueur1":"1",
        "points1": '4',
        'points2': '7',
        'joueur2':'2'
    }, follow_redirects=True)
    assert b"Tournois internes" in response.data
    assert "/competitions/tournois-internes/" in response.request.path

def test_internes_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournois-internes/2/delete/")
        response = client.post('/competitions/tournois-internes/2/delete/', follow_redirects=True)
        assert b"Tournois internes" in response.data
