import pytest
from appli import app

@pytest.fixture
def testapp():
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })

    with app.app_context():
        pass

    yield app

@pytest.fixture
def client(testapp):
    return testapp.test_client()
