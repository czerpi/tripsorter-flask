import unittest
import pytest
from app import create_app

url = 'http://127.0.0.1:5000'  # The root url of the flask app


@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app()
    yield app.test_client()
