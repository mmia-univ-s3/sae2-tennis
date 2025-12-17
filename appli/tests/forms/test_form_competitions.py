from datetime import datetime, date
# pylint: disable=missing-function-docstring

# pylint: disable=duplicate-code
def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)


def test_form_tournoi_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/individuel/4/delete/")
        response = client.post('/competitions/tournoi/individuel/4/delete/',
            follow_redirects=True)

        assert response.status_code == 200
        assert "/competitions/calendrier/" in response.request.path
        assert b"Championnat individuel 4" not in response.data

        response = login(client, "/competitions/tournoi/equipe/4/delete/")
        response = client.post('/competitions/tournoi/equipe/4/delete/',
            follow_redirects=True)

        assert response.status_code == 200
        assert "/competitions/calendrier/" in response.request.path
        assert b"championnat equipe 4" not in response.data


def test_form_tournoi_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/individuel/3/update/")
        response = client.post('/competitions/tournoi/individuel/3/update/',
            follow_redirects=True, data={"titre" : "Championnat individuel 1112",
                                         "date_championnat" : date.today(), "categorie" : "Jeune",
                                         "serie" : "Garçon", "niveau" : "Départemental"})

        assert response.status_code == 200
        assert "/competitions/calendrier/" in response.request.path
        assert b"Championnat individuel 3" not in response.data
        assert b"Championnat individuel 1112" in response.data

        response = login(client, "/competitions/tournoi/equipe/3/update/")
        response = client.post('/competitions/tournoi/equipe/3/update/',
            follow_redirects=True, data={"titre" : "championnat equipe 1112",
                                         "date_championnat" : date.today(), "categorie" : "Jeune",
                                         "serie" : "Garçon"})

        assert response.status_code == 200
        assert "/competitions/calendrier/" in response.request.path
        assert b"championnat equipe 3" not in response.data
        assert b"championnat equipe 1112" in response.data


def test_form_tournoi_add(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/individuel/add/")
        response = client.post('/competitions/tournoi/individuel/add/',
            follow_redirects=True, data={"titre" : "Championnat individuel 1111",
                                         "date_championnat" : date.today(), "categorie" : "Jeune",
                                         "serie" : "Garçon", "niveau" : "Départemental"})

        assert response.status_code == 200
        assert "/competitions/calendrier/" in response.request.path
        assert b"Championnat individuel 1111" in response.data

        response = login(client, "/competitions/tournoi/equipe/add/")
        response = client.post('/competitions/tournoi/equipe/add/',
            follow_redirects=True, data={"titre" : "championnat equipe 1111",
                                         "date_championnat" : date.today(), "categorie" : "Jeune",
                                         "serie" : "Garçon"})

        assert response.status_code == 200
        assert "/competitions/calendrier/" in response.request.path
        assert b"championnat equipe 1111" in response.data


def test_form_participant_indiv_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/individuel/1/3/delete/")
        response = client.post('/competitions/tournoi/individuel/1/3/delete/',
            follow_redirects=True)

        assert response.status_code == 200
        assert "/competitions/tournoi/individuel/1/" in response.request.path
        assert b"Jean Michel" not in response.data


def test_form_participant_indiv_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/individuel/1/1/update/")
        response = client.post('/competitions/tournoi/individuel/1/1/update/',
            follow_redirects=True, data={"joueur" : 1, "rang" : "1er"})

        assert response.status_code == 200
        assert "/competitions/tournoi/individuel/1/" in response.request.path
        assert b"1er" in response.data


def test_form_participant_indiv_add(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/individuel/2/add/")
        response = client.post('/competitions/tournoi/individuel/2/add/',
            follow_redirects=True, data={"joueur" : 1, "rang" : "1er"})

        assert response.status_code == 200
        assert "/competitions/tournoi/individuel/2/" in response.request.path
        assert b"Jean Claude" in response.data


def test_form_participant_equipe_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/equipe/6/6/delete/")
        response = client.post('/competitions/tournoi/equipe/6/6/delete/',
            follow_redirects=True)

        assert response.status_code == 200
        assert "/competitions/tournoi/equipe/6/" in response.request.path
        assert b"Equipe : equipe 6" not in response.data


def test_form_participant_equipe_update(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/equipe/2/2/update/")
        response = client.post('/competitions/tournoi/equipe/2/2/update/',
            follow_redirects=True, data={"equipe" : 2, "rang" : "1er", "poule" : "A"})

        assert response.status_code == 200
        assert "/competitions/tournoi/equipe/2/" in response.request.path
        assert b"Classement : 1er" in response.data


def test_form_participant_equipe_add(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/equipe/2/add/")
        response = client.post('/competitions/tournoi/equipe/2/add/',
            follow_redirects=True, data={"equipe" : 1, "rang" : "1er", "poule" : "D"})

        assert response.status_code == 200
        assert "/competitions/tournoi/equipe/2/" in response.request.path
        assert b"equipe 1" in response.data


def test_form_affronter_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournoi/equipe/3/3/06-10-2025/delete/")
        response = client.post('/competitions/tournoi/equipe/3/3/06-10-2025/delete/',
            follow_redirects=True)

        assert response.status_code == 200
        assert "/competitions/tournoi/equipe/3/" in response.request.path
        assert b"06/10/2025" not in response.data


def test_form_affronter_update(client, testapp):
    with testapp.app_context():
        #Test dans le cas où la modification s'est bien effectuée
        response = login(client, "/competitions/tournoi/equipe/5/5/08-10-2025/update/")
        response = client.post('/competitions/tournoi/equipe/5/5/08-10-2025/update/',
            follow_redirects=True, data={"adversaire" : "equipe 4", "date" : date.today(),
                                         "resultat": 'D', "score" : "10/12", "domicile" : "True"})

        assert response.status_code == 200
        assert "/competitions/tournoi/equipe/5/" in response.request.path
        assert f"{date.today().strftime('%d/%m/%Y')}".encode("utf-8") in response.data

        #Test dans le cas où la modification ne s'est pas bien effectuée
        response = login(client, "/competitions/tournoi/equipe/11/12/26-03-2023/update/")
        response = client.post('/competitions/tournoi/equipe/11/12/26-03-2023/update/',
            follow_redirects=True, data={"adversaire" : "Malemort ASV",
                                         "date" : datetime.strptime("02-04-2023", "%d-%m-%Y")\
                                            .date(),
                                         "resultat": 'D', "score" : "10/12", "domicile" : "True"})

        assert response.status_code == 200
        assert "/competitions/tournoi/equipe/11/12/26-03-2023/update/" in response.request.path
        assert b"Modification du match" in response.data


def test_form_affronter_add(client, testapp):
    with testapp.app_context():
        #Test dans le cas où l'ajout s'est bien effectué
        response = login(client, "/competitions/tournoi/equipe/3/3/add/")
        response = client.post('/competitions/tournoi/equipe/3/3/add/',
            follow_redirects=True, data={"adversaire" : "adversaire1", "date" : date.today(),
                                         "resultat": 'D', "score" : "10/12", "domicile" : "True"})

        assert response.status_code == 200
        assert "/competitions/tournoi/equipe/3/" in response.request.path
        assert b"adversaire1" in response.data

        #Test dans le cas où l'ajout ne s'est pas effectué
        response = login(client, "/competitions/tournoi/equipe/5/5/add/")
        response = client.post('/competitions/tournoi/equipe/5/5/add/',
            follow_redirects=True, data={"adversaire" : "adversaire1", "date" : date.today(),
                                         "resultat": 'D', "score" : "10/12", "domicile" : "True"})

        assert response.status_code == 200
        assert "/competitions/tournoi/equipe/5/5/add/" in response.request.path
        assert b"Ajout d'un match" in response.data


def test_form_interne_add(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournois-internes/add/")
        response = client.post('competitions/tournois-internes/add/', data={
            "date":"2025-12-14",
            "titre":"Test",
            "serie":"test",
            "joueur1":"1",
            "points1": '4',
            'points2': '7',
            'joueur2':'2'
        }, follow_redirects=True)
        assert "/competitions/tournois-internes/" in response.request.path


def test_form_interne_add_error(client, testapp):
    with testapp.app_context():
        response = login(client, "/competitions/tournois-internes/add/")
        response = client.post('competitions/tournois-internes/add/', data={
            "date":"2025-12-14",
            "titre":"Test",
            "serie":"test",
            "joueur1":"1",
            "points1": '4',
            'points2': '7',
            'joueur2':'1'
        }, follow_redirects=True)
        assert "/competitions/tournois-internes/add/" in response.request.path
