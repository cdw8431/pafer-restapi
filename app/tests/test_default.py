from core.config import settings
from fastapi.testclient import TestClient
from main import app

api_str = settings.API_V1_STR
client = TestClient(app)

user_data = {"email": "test@email.com", "nickname": "test", "password": "testpassword"}


def test_redirect_root_to_docs():
    res = client.get("/")
    assert res.status_code == 200
    assert res.url == "http://testserver/docs"
