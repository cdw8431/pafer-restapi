from fastapi.testclient import TestClient

from config import settings
from main import app

client = TestClient(app)


def test_read_users():
    res = client.get(f"{settings.API_V1_STR}/users")
    assert res.status_code == 200
    res_results = res.json()
    if res_results:
        assert isinstance(res_results, list) and ["id", "email", "created"] == list(
            res_results[0].keys()
        )
