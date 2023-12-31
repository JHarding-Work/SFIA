from app import app
from models import *
from flask import session
from flask_testing import TestCase


class TestBase(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    TESTING = True

    def create_app(self):
        # Pass in testing configurations for the app.
        # Here we use sqlite without a persistent database for our tests.
        app.config.update(
              SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
              SECRET_KEY='TEST_SECRET_KEY',
              DEBUG=True,
              WTF_CSRF_ENABLED=False
        )
        return app

    def setUp(self) -> None:
        db.create_all()
        self.setUpTestData()

    def setUpTestData(self):
        pass

    # Will be called after every test
    def tearDown(self):
        # Close the database session and remove all contents of the database
        db.session.remove()
        db.drop_all()
