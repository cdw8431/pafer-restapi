import os

from config import settings
from fastapi.testclient import TestClient
from jose import jwt
from main import app

client = TestClient(app)

data = {"email": "test@email.com", "password": "testpassword"}


def test_register_user():
    res = client.post(f"{settings.API_V1_STR}/users/register", json=data)
    assert res.status_code == 200
    access_token = res.json().get("access_token")
    SECRET_KEY, ALGORITHM = os.getenv("SECRET_KEY"), os.getenv("ALGORITHM")
    assert access_token and data.get("email") == jwt.decode(
        access_token, SECRET_KEY, algorithms=[ALGORITHM]
    ).get("sub")


def test_register_user_invalid1():
    res = client.post(f"{settings.API_V1_STR}/users/register", json=data)
    assert res.status_code == 400


def test_read_users():
    res = client.get(f"{settings.API_V1_STR}/users")
    result = [row for row in res.json() if row.get("email") == data.get("email")]
    is_success = result and result[0].get("email") == data.get("email")
    assert res.status_code == 200
    assert is_success
    if is_success:
        data["id"] = result[0].get("id")


def test_read_user_by_id():
    res = client.get(f"{settings.API_V1_STR}/users/{data.get('id')}")
    assert res.status_code == 200
    assert res.json().get("email") == data.get("email")


def test_update_user():
    res = client.put(
        f"{settings.API_V1_STR}/users/{data.get('id')}",
        json={"password": "newtestpassword"},
    )
    assert res.status_code == 200
    assert res.json() == {"msg": "success"}


def test_delete_user_by_id():
    res = client.delete(f"{settings.API_V1_STR}/users/{data.get('id')}")
    assert res.status_code == 200
    assert res.json() == {"msg": "success"}
