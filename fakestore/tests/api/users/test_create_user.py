import pytest

from helpers import EXISTING_USER_IDS, brief


def new_user(name):
    return {"username": name, "email": f"{name}@example.com", "password": "Passw0rd!"}


@pytest.mark.smoke
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_USERS_008_create_user(api, unique):
    r = api.post("/users", json=new_user(unique()))
    assert r.status_code == 201, brief(r)
    assert isinstance(r.json().get("id"), int)


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_USERS_009_create_user_response_returns_the_user(api, unique):
    data = new_user(unique())
    body = api.post("/users", json=data).json()
    missing = [k for k in ("username", "email") if body.get(k) != data[k]]
    assert not missing, f"spec: 201 returns the User; response is {body} (missing {missing})"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_010_new_user_never_gets_an_existing_users_id(api, unique):
    ids = [api.post("/users", json=new_user(unique())).json().get("id") for _ in range(5)]
    clashes = [i for i in ids if i in EXISTING_USER_IDS]
    assert not clashes, f"5 new users got ids {ids}; {len(clashes)} reuse an existing user's id"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_011_create_user_with_empty_body_returns_400(api):
    r = api.post("/users", json={})
    assert r.status_code == 400, f"a user with no data should be rejected, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_012_create_user_with_invalid_email_returns_400(api, unique):
    r = api.post("/users", json={**new_user(unique()), "email": "not-an-email"})
    assert r.status_code == 400, f"email 'not-an-email' should be rejected, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_013_create_user_without_password_returns_400(api, unique):
    data = new_user(unique())
    del data["password"]
    r = api.post("/users", json=data)
    assert r.status_code == 400, f"a user without password should be rejected, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_014_create_user_with_existing_username_is_rejected(api):
    existing = api.get("/users/2").json()["username"]
    r = api.post("/users", json=new_user(existing))
    assert r.status_code in (400, 409), f"username {existing!r} already exists, got {brief(r)}"
