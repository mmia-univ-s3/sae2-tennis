# pylint: disable=missing-function-docstring

# pylint: disable=duplicate-code
def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)


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
