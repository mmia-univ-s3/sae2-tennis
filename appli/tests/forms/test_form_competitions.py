# pylint: disable=duplicate-code
def login(client, next):
    return client.post('/connexion/', data={
        "login": "michel",
        "password": "1",
        "next": next
    }, follow_redirects=True)
    
