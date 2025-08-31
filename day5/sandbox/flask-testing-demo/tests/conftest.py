import pytest
from api.app import create_app
from api.extensions import db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # in-memory DB for tests
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A CLI runner for the app"""
    return app.test_cli_runner()