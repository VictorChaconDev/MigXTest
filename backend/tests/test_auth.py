def test_register_user_success(client):
    response = client.post(
        "/auth/register", json={"username": "testuser", "password": "securepassword"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_username_fails(client):
    # Register once
    response1 = client.post(
        "/auth/register", json={"username": "dupuser", "password": "password123"}
    )
    assert response1.status_code == 201

    # Register again with same username
    response2 = client.post(
        "/auth/register", json={"username": "dupuser", "password": "password123"}
    )
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Username already registered"


def test_login_success(client):
    # Register user first
    client.post(
        "/auth/register", json={"username": "loginuser", "password": "mypassword"}
    )

    # Login
    response = client.post(
        "/auth/token", data={"username": "loginuser", "password": "mypassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    # Try logging in with non-existent user
    response = client.post(
        "/auth/token", data={"username": "nonexistent", "password": "password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
