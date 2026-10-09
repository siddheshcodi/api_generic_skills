import pytest

from helpers import brief


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_USERS_005_create_user(api, unique):
    name = unique()
    r = api.post("/users", json={"username": name, "email": f"{name}@example.com", "password": "Passw0rd!"})
    assert r.status_code == 201, brief(r)
    assert isinstance(r.json().get("id"), int)


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_006_create_user_with_invalid_email_returns_400(api, unique):
    r = api.post("/users", json={"username": unique(), "email": "not-an-email", "password": "Passw0rd!"})
    assert r.status_code == 400, f"expected 400 for email 'not-an-email', got {brief(r)}"
