import os

from config import settings
from fastapi.testclient import TestClient
from jose import jwt
from main import app

client = TestClient(app)

data = {"email": "test@email.com", "password": "testpassword"}


def test_get_user_by_id_invalid1():
    # user does not exists
    res = client.get(f"{settings.API_V1_STR}/users/-1")
    assert res.status_code == 404


def test_get_user_by_email_invalid1():
    # user does not exists
    res = client.get(f"{settings.API_V1_STR}/users/email/{data.get('email')}")
    assert res.status_code == 404


def test_update_user_password_invalid1():
    # user does not exists
    res = client.patch(
        f"{settings.API_V1_STR}/users/-1/change-password",
        json={"oldpassword": data.get("password"), "newpassword": "newtestpassword"},
    )
    assert res.status_code == 404


def test_post_user():
    res = client.post(f"{settings.API_V1_STR}/users", json=data)
    assert res.status_code == 201
    access_token = res.json().get("access_token")
    SECRET_KEY, ALGORITHM = os.getenv("SECRET_KEY"), os.getenv("ALGORITHM")
    assert access_token and data.get("email") == jwt.decode(
        access_token, SECRET_KEY, algorithms=[ALGORITHM]
    ).get("sub")


def test_post_user_invalid1():
    res = client.post(f"{settings.API_V1_STR}/users", json=data)
    assert res.status_code == 400
    assert res.json() == {"detail": "This email already exists."}


def test_get_users():
    res = client.get(f"{settings.API_V1_STR}/users")
    result = [row for row in res.json() if row.get("email") == data.get("email")]
    is_success = result and result[0].get("email") == data.get("email")
    assert res.status_code == 200
    assert is_success
    if is_success:
        data["id"] = result[0].get("id")


def test_get_user_by_id():
    res = client.get(f"{settings.API_V1_STR}/users/{data.get('id')}")
    assert res.status_code == 200
    assert res.json().get("email") == data.get("email")


def test_get_user_by_email():
    res = client.get(f"{settings.API_V1_STR}/users/email/{data.get('email')}")
    assert res.status_code == 200
    assert res.json().get("email") == data.get("email")


def test_update_user_password():
    res = client.patch(
        f"{settings.API_V1_STR}/users/{data.get('id')}/change-password",
        json={"oldpassword": data.get("password"), "newpassword": "newtestpassword"},
    )
    assert res.status_code == 200
    assert res.json() == {"msg": "success"}


def test_update_user_password_invalid2():
    res = client.patch(
        f"{settings.API_V1_STR}/users/{data.get('id')}/change-password",
        json={"oldpassword": data.get("password"), "newpassword": "newtestpassword"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Password does not match."}


def test_delete_user_by_id():
    res = client.delete(f"{settings.API_V1_STR}/users/{data.get('id')}")
    assert res.status_code == 204
