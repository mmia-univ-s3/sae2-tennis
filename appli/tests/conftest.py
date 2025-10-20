import pytest
from appli import appli

@pytest.fixture
def testapp():
    appli.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })

    with appli.app_context():
        pass

    yield appli

    # with app.app_context():
    #     db.drop_all()

@pytest.fixture
def client(testapp):
    return testapp.test_client()
