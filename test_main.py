import unittest

from app.middleware.authenticate import authenticate
from app.middleware.jwt_handler import create_access_token  , verify_token
from app.services.helper import send_otp_to_email

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
        data = verify_token(self.token)
        self.assertEqual(int , type(data))
        
    def test_authenticate(self):
        data = authenticate(self.token)
        self.assertEqual(1 , data)
        
    def test_email(self):
        value = send_otp_to_email("oboirientijani.com" , "tijanioboiriendev@gmail.com" , 1 , "HNG")
        print(value)