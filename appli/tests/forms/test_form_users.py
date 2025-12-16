# pylint: disable=duplicate-code
def login(client, callback):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": callback
    }, follow_redirects=True)

def test_forms_user_create(client, testapp):
    with testapp.app_context():
        response = login(client, "/utilisateurs/create/")
        response = client.post('/utilisateurs/create/', data={
            "login":"truc123",
            "password":"bidule123",
            "repeat_password":"bidule123"}
            , follow_redirects=True)

        assert response.status_code == 200
        assert "/utilisateurs/" in response.request.path
        assert b"truc" in response.data
        assert b"martin" in response.data

def test_forms_user_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/utilisateurs/jean/delete/")
        response = client.post('/utilisateurs/jean/delete/', follow_redirects=True)

        assert response.status_code == 200
        assert "/utilisateurs/" in response.request.path
        assert b"jean" not in response.data

def test_forms_user_reset(client, testapp):
    with testapp.app_context():
        response = login(client, "/utilisateurs/caillou/reset/")
        response = client.post('/utilisateurs/caillou/reset/', follow_redirects=True)

        assert response.status_code == 200
        assert "/utilisateurs/" in response.request.path
        assert b"caillou" in response.data

def test_forms_user_create_bad(client, testapp):
    with testapp.app_context():
        response = login(client, "/utilisateurs/create/")
        response = client.post('/utilisateurs/create/', data={
            "login":"truc",
            "password":"bidule",
            "repeat_password":"bad"}
            , follow_redirects=True)

        assert response.status_code == 200
        assert "/utilisateurs/create/" in response.request.path
        assert b"truc" in response.data

def test_forms_user_auto_delete(client, testapp):
    with testapp.app_context():
        response = login(client, "/utilisateurs/michel/delete/")
        response = client.post('/utilisateurs/michel/delete/', follow_redirects=True)

        assert response.status_code == 200
        assert "/utilisateurs/" in response.request.path
        assert b"michel" in response.data
