import unittest

from app.middleware.authenticate import authenticate
from app.middleware.jwt_handler import create_access_token  , verify_access_token

class Request:
    def __init__(self , token) -> None:
        self.token = token
        
    @property
    def headers(self):
        return {"Authorization" : f"Bearer {self.token}"}
    

class TestsCases(unittest.TestCase):
    def setUp(self) -> None:
        self.token = create_access_token(1)
    
    def test_very_token(self):
        data = verify_access_token(self.token)
        self.assertEqual(dict , type(data))
        
    def test_authenticate(self):
        data = authenticate(Request(self.token))
        self.assertEqual(1 , data)