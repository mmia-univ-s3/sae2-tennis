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
    assert "03/11/2025".encode("utf-8") in response.data
    assert "Championnat individuel 1".encode("utf-8") in response.data

def test_tournoi_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/12/delete/")
        response = client.get('/competitions/tournoi/12/delete/', follow_redirects=True)
        assert b"Suppression du tournoi Championnat individuel 1" in response.data
        response = login(client, "/competitions/tournoi/1/delete/")
        response = client.get('/competitions/tournoi/1/delete/', follow_redirects=True)
        assert b"Suppression du tournoi championnat equipe 1" in response.data

def test_tournoi_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/12/update/")
        response = client.get('/competitions/tournoi/12/update/', follow_redirects=True)
        assert b"Modification du tournoi Championnat individuel 1" in response.data
        response = login(client, "/competitions/tournoi/1/update/")
        response = client.get('/competitions/tournoi/1/update/', follow_redirects=True)
        assert b"Modification du tournoi championnat equipe 1" in response.data

def test_tournoi_add(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/individuel/add/")
        response = client.get('/competitions/tournoi/individuel/add/', follow_redirects=True)
        assert b"Ajout d'un tournoi" in response.data
        assert b"Vous allez ajouter un tournoi individuel." in response.data
        response = login(client, "/competitions/tournoi/equipe/add/")
        response = client.get('/competitions/tournoi/equipe/add/', follow_redirects=True)
        assert b"Ajout d'un tournoi" in response.data
        assert b"Vous allez ajouter un tournoi par " in response.data
        assert b"quipe." in response.data

def test_tournoi(client, testapp):
    with testapp.app_context():
        response = client.get('/competitions/tournoi/12/', follow_redirects=True)
        assert b"Championnat individuel 1" in response.data
        response = client.get('/competitions/tournoi/1/', follow_redirects=True)
        assert b"championnat equipe 1" in response.data

def test_participant_indiv_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/12/1/delete/")
        response = client.get('/competitions/tournoi/12/1/delete/',
                              follow_redirects=True)
        assert b"Suppression d'un participant pour Championnat individuel 1" in response.data
        assert b"Jean Claude" in response.data

def test_participant_indiv_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/12/1/update/")
        response = client.get('/competitions/tournoi/12/1/update/',
                              follow_redirects=True)
        assert b"Modification du participant Jean Claude pour Championnat individuel 1" \
               in response.data

def test_participant_indiv_add(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/12/add/")
        response = client.get('/competitions/tournoi/12/add/', follow_redirects=True)
        assert b"Ajout d'un participant pour Championnat individuel 1" in response.data

def test_participant_equipe_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/1/1/delete/")
        response = client.get('/competitions/tournoi/1/1/delete/', follow_redirects=True)
        assert b"Suppression d'une " in response.data
        assert b"quipe pour championnat equipe 1" in response.data
        assert b"equipe 1" in response.data

def test_participant_equipe_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/1/1/update/")
        response = client.get('/competitions/tournoi/1/1/update/', follow_redirects=True)
        assert b"Modification de l'" in response.data
        assert b"quipe equipe 1 pour championnat equipe 1" in response.data

def test_participant_equipe_add(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/1/add/")
        response = client.get('/competitions/tournoi/1/add/', follow_redirects=True)
        assert b"Ajout d'une " in response.data
        assert b"quipe pour championnat equipe 1" in response.data
        assert b"equipe 2" in response.data

def test_affronter_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/1/1/05-10-2025/delete/")
        response = client.get('/competitions/tournoi/1/1/05-10-2025/delete/',
                              follow_redirects=True)
        assert (b"Suppression du match equipe 1 contre equipe 10 dans le championnat "
                b"equipe 1 le 05-10-2025") in response.data
        assert b"equipe 10" in response.data

def test_affronter_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/1/1/05-10-2025/update/")
        response = client.get('/competitions/tournoi/1/1/05-10-2025/update/',
                              follow_redirects=True)
        assert (b"Modification du match equipe 1 contre equipe 10 dans le championnat "
                b"equipe 1 le 05-10-2025") in response.data
        assert b"equipe 10" in response.data

def test_affronter_add(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/1/1/add/")
        response = client.get('/competitions/tournoi/1/1/add/',
                              follow_redirects=True)
        assert b"Ajout d'un match de equipe 1 dans le championnat equipe 1" in response.data

def test_palmares_list(client):
    response = client.get('/competitions/palmares/list/', follow_redirects=True)
    assert b"Palmar" in response.data
    assert b"2025" in response.data

def test_palmares_annee(client, testapp):
    with testapp.app_context():
        response = client.get('/competitions/palmares/2025/',
                              follow_redirects=True)
        assert b"Championnat Individuel D" in response.data
        assert b"partemental" in response.data
        assert b"Championnat individuel 1" in response.data
        assert b"Jean Claude" in response.data
        assert b"championnat equipe 1" in response.data
        assert b"11/14 ans G" in response.data
        assert b"10 Departemental 2" in response.data

def test_tournois_internes(client):
    response = client.get('/competitions/tournois-internes/', follow_redirects=True)
    assert b"Championnat interne 1" in response.data

def test_internes_add(client):
    response = login(client, "/competitions/tournois-internes/add/")
    response = client.get('competitions/tournois-internes/add/', follow_redirects=True)
    assert b"Ajout d'un tournoi interne" in response.data

def test_internes_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournois-internes/21/")
        response = client.post('competitions/tournois-internes/21/', data={
            "date":"2025-12-14",
            "titre":"Testytest",
        }, follow_redirects=True)
        assert b"Testytest" in response.data
        assert "/competitions/tournois-internes/" in response.request.path

def test_internes_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournois-internes/delete/21/")
        response = client.post('/competitions/tournois-internes/delete/21/', follow_redirects=True)
        assert b"Testytest" not in response.data
