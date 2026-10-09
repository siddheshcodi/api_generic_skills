"""Login -> identify the user -> use their data in other modules."""
import pytest

from helpers import jwt_claims


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_INTEGRATION_001_token_subject_is_the_logged_in_user(api, token, login_creds):
    user = api.get(f"/users/{jwt_claims(token)['sub']}").json()
    assert user["username"] == login_creds["username"]


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEGRATION_002_logged_in_user_can_see_own_carts(api, token):
    uid = jwt_claims(token)["sub"]
    carts = api.get(f"/carts/user/{uid}").json()
    assert carts and all(c["userId"] == uid for c in carts)
