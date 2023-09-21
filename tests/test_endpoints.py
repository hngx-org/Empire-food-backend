from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_search():
    response = client.get("/api/user/search/test@gmail.com")
    assert response.status_code == 200
    assert response.json() == {
    "message": "User search successful",
    "statusCode": 200,
    "data": []
}