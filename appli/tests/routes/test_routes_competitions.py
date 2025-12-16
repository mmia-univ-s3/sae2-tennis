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
