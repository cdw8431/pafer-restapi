import os

from jose import jwt
from tests.test_default import api_str, client, user_data


def test_get_user_by_id_invalid1():
    # user does not exists
    res = client.get(f"{api_str}/users/-1")
    assert res.status_code == 404


def test_get_user_by_email_invalid1():
    # user does not exists
    res = client.get(f"{api_str}/users/email/{user_data.get('email')}")
    assert res.status_code == 404


def test_update_user_password_invalid1():
    # user does not exists
    res = client.patch(
        f"{api_str}/users/-1/change-password",
        json={
            "oldpassword": user_data.get("password"),
            "newpassword": "newtestpassword",
        },
    )
    assert res.status_code == 404


def test_post_user_login_invalid1():
    # user does not exists
    res = client.post(f"{api_str}/auth/login", json=user_data)
    assert res.status_code == 404


def test_post_user_register():
    res = client.post(f"{api_str}/users", json=user_data)
    assert res.status_code == 201
    access_token = res.json().get("access_token")
    SECRET_KEY, ALGORITHM = os.getenv("SECRET_KEY"), os.getenv("ALGORITHM")
    assert access_token and user_data.get("email") == jwt.decode(
        access_token, SECRET_KEY, algorithms=[ALGORITHM]
    ).get("sub")


def test_post_user_register_invalid1():
    res = client.post(f"{api_str}/users", json=user_data)
    assert res.status_code == 400
    assert res.json() == {"detail": "This user already exists."}


def test_get_users():
    res = client.get(f"{api_str}/users")
    result = [row for row in res.json() if row.get("email") == user_data.get("email")]
    is_success = result and result[0].get("email") == user_data.get("email")
    assert res.status_code == 200
    assert is_success
    if is_success:
        user_data["id"] = result[0].get("id")


def test_get_user_by_id():
    res = client.get(f"{api_str}/users/{user_data.get('id')}")
    assert res.status_code == 200
    assert res.json().get("email") == user_data.get("email")


def test_get_user_by_email():
    res = client.get(f"{api_str}/users/email/{user_data.get('email')}")
    assert res.status_code == 200
    assert res.json().get("email") == user_data.get("email")


def test_post_user_login():
    res = client.post(f"{api_str}/auth/login", json=user_data)
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_update_user_password():
    res = client.patch(
        f"{api_str}/users/{user_data.get('id')}/change-password",
        json={
            "oldpassword": user_data.get("password"),
            "newpassword": "newtestpassword",
        },
    )
    assert res.status_code == 200
    assert res.json() == {"msg": "success"}


def test_post_user_login_invalid2():
    res = client.post(f"{api_str}/auth/login", json=user_data)
    assert res.status_code == 403


def test_update_user_password_invalid2():
    res = client.patch(
        f"{api_str}/users/{user_data.get('id')}/change-password",
        json={
            "oldpassword": user_data.get("password"),
            "newpassword": "newtestpassword",
        },
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Password does not match."}


def test_delete_user_by_id():
    res = client.delete(f"{api_str}/users/{user_data.get('id')}")
    assert res.status_code == 204
