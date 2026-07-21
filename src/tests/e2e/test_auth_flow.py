async def _register_and_login(client, email: str) -> dict:
    await client.post(
        "/auth/register",
        json={
            "username": "user_" + email.split("@")[0],
            "email": email,
            "password": "secret123",
        },
    )
    response = await client.post(
        "/auth/login", json={"email": email, "password": "secret123"}
    )
    return response.json()


async def test_register_then_login(client):
    r = await client.post(
        "/auth/register",
        json={"username": "john", "email": "john@example.com", "password": "secret123"},
    )
    assert r.status_code == 201
    assert r.json()["role"] == "user"

    r = await client.post(
        "/auth/login", json={"email": "john@example.com", "password": "secret123"}
    )
    assert r.status_code == 200
    assert "access_token" in r.json()


async def test_login_wrong_password(client):
    await _register_and_login(client, "kate@example.com")
    r = await client.post(
        "/auth/login", json={"email": "kate@example.com", "password": "nope"}
    )
    assert r.status_code == 401


async def test_access_token_rejected_on_refresh(client):
    tokens = await _register_and_login(client, "a@example.com")
    r = await client.post(
        "/tokens/refresh", json={"refreshToken": tokens["access_token"]}
    )
    assert r.status_code == 401


async def test_refresh_rotation_and_revocation(client):
    tokens = await _register_and_login(client, "b@example.com")
    refresh = tokens["refresh_token"]

    first = await client.post("/tokens/refresh", json={"refreshToken": refresh})
    assert first.status_code == 200

    reused = await client.post("/tokens/refresh", json={"refreshToken": refresh})
    assert reused.status_code == 401


async def test_users_endpoint_requires_admin(client):
    tokens = await _register_and_login(client, "plain@example.com")
    r = await client.get(
        "/users/", headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    assert r.status_code == 403


async def test_admin_creates_and_blocks_user(client, admin_token):
    auth = {"Authorization": f"Bearer {admin_token}"}

    created = await client.post(
        "/users/",
        headers=auth,
        json={
            "username": "target",
            "email": "target@example.com",
            "password": "secret123",
            "role": "advanced",
        },
    )
    assert created.status_code == 201
    user_id = created.json()["id"]

    blocked = await client.patch(
        f"/users/{user_id}", headers=auth, json={"is_blocked": True}
    )
    assert blocked.status_code == 200
    assert blocked.json()["is_blocked"] is True

    login = await client.post(
        "/auth/login", json={"email": "target@example.com", "password": "secret123"}
    )
    assert login.status_code == 403
