def test_calendrier(client):
    response = client.get('/competitions/calendrier/', follow_redirects=True)
    assert b"Calendrier et r" in response.data
    assert b"sultats" in response.data
    
def test_palmares(client):
    response = client.get('/competitions/palmares/', follow_redirects=True)
    assert b"Palmar" in response.data
    
def test_tournois(client):
    response = client.get('/competitions/tournois/', follow_redirects=True)
    assert b"Tournois" in response.data
    
def test_tournois_internes(client):
    response = client.get('/competitions/tournois-internes/', follow_redirects=True)
    assert b"Tournois internes" in response.data