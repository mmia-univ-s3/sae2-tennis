# pylint: disable=missing-function-docstring

# pylint: disable=duplicate-code
def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)

def test_calendrier(client):
    response = client.get('/competitions/calendrier/', follow_redirects=True)
    assert "Calendrier des compétitions".encode("utf-8") in response.data

def test_tournoi_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/individuel/12/delete/")
        response = client.get('/competitions/tournoi/individuel/12/delete/', follow_redirects=True)
        assert b"Suppression du tournoi" in response.data
        response = login(client, "/competitions/tournoi/equipe/1/delete/")
        response = client.get('/competitions/tournoi/equipe/1/delete/', follow_redirects=True)
        assert b"Suppression du tournoi" in response.data

def test_tournoi_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/individuel/12/update/")
        response = client.get('/competitions/tournoi/individuel/12/update/', follow_redirects=True)
        assert b"Modification du tournoi" in response.data
        response = login(client, "/competitions/tournoi/equipe/1/update/")
        response = client.get('/competitions/tournoi/equipe/1/update/', follow_redirects=True)
        assert b"Modification du tournoi" in response.data

def test_tournoi_add(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/individuel/add/")
        response = client.get('/competitions/tournoi/individuel/add/', follow_redirects=True)
        assert "Ajout d'un tournoi".encode("utf-8") in response.data
        response = login(client, "/competitions/tournoi/equipe/add/")
        response = client.get('/competitions/tournoi/equipe/add/', follow_redirects=True)
        assert "Ajout d'un tournoi".encode("utf-8") in response.data

def test_tournoi(client, testapp):
    with testapp.app_context():
        response = client.get('/competitions/tournoi/individuel/12/', follow_redirects=True)
        assert b"Championnnat individuel" in response.data
        response = client.get('/competitions/tournoi/equipe/1/', follow_redirects=True)
        assert "Championnat par équipe".encode("utf-8") in response.data

def test_participant_indiv_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/individuel/12/1/delete/")
        response = client.get('/competitions/tournoi/individuel/12/1/delete/',
                              follow_redirects=True)
        assert "Suppression d'un participant".encode("utf-8") in response.data

def test_participant_indiv_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/individuel/12/1/update/")
        response = client.get('/competitions/tournoi/individuel/12/1/update/',
                              follow_redirects=True)
        assert b"Modification du participant" in response.data

def test_participant_indiv_add(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/individuel/12/add/")
        response = client.get('/competitions/tournoi/individuel/12/add/', follow_redirects=True)
        assert "Ajout d'un participant".encode("utf-8") in response.data

def test_participant_equipe_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/equipe/1/1/delete/")
        response = client.get('/competitions/tournoi/equipe/1/1/delete/', follow_redirects=True)
        assert "Suppression d'une équipe".encode("utf-8") in response.data

def test_participant_equipe_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/equipe/1/1/update/")
        response = client.get('/competitions/tournoi/equipe/1/1/update/', follow_redirects=True)
        assert "Modification de l'équipe".encode("utf-8") in response.data

def test_participant_equipe_add(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/equipe/1/add/")
        response = client.get('/competitions/tournoi/equipe/1/add/', follow_redirects=True)
        assert "Ajout d'une équipe".encode("utf-8") in response.data

def test_affronter_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/equipe/1/1/05-10-2025/delete/")
        response = client.get('/competitions/tournoi/equipe/1/1/05-10-2025/delete/',
                              follow_redirects=True)
        assert b"Suppression du match" in response.data

def test_affronter_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/equipe/1/1/05-10-2025/update/")
        response = client.get('/competitions/tournoi/equipe/1/1/05-10-2025/update/',
                              follow_redirects=True)
        assert b"Modification du match" in response.data

def test_affronter_add(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/equipe/1/1/add/")
        response = client.get('/competitions/tournoi/equipe/1/1/add/',
                              follow_redirects=True)
        assert b"Ajout d'un match" in response.data

def test_palmares_list(client):
    response = client.get('/competitions/palmares/list/', follow_redirects=True)
    assert "Palmarès".encode("utf-8") in response.data

def test_palmares_annee(client, testapp):
    with testapp.app_context():
        response = client.get('/competitions/palmares/2025/',
                              follow_redirects=True)
        assert "Palmarès - 2025".encode("utf-8") in response.data

def test_tournois_internes(client):
    response = client.get('/competitions/tournois-internes/', follow_redirects=True)
    assert b"Tournois internes" in response.data

def test_internes_add(client):
    response = login(client, "/competitions/tournois-internes/add/")
    response = client.get('competitions/tournois-internes/add/', follow_redirects=True)
    assert b"Ajout d'un tournoi interne" in response.data

def test_internes_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournois-internes/21/")
        response = client.post('competitions/tournois-internes/21/', data={
            "date":"2025-12-14",
            "titre":"Test",
        }, follow_redirects=True)
        assert b"Tournois internes" in response.data
        assert "/competitions/tournois-internes/" in response.request.path

def test_internes_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournois-internes/delete/21/")
        response = client.post('/competitions/tournois-internes/delete/21/', follow_redirects=True)
        assert b"Tournois internes" in response.data
