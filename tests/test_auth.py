from fastapi.testclient import TestClient
from main import app

""""
This module tests all auth routes of the free lunch endpoint
"""

client = TestClient(app)

def test_user_signup():
    pass
