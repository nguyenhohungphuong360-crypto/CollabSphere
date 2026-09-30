def test_register_success(client):
    res = client.post('/auth/register', json={
        "user_name": "developer_john",
        "password": "strongPassword123",
        "description": "Senior Developer"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "token" in data
    assert data["user"]["user_name"] == "developer_john"


def test_register_duplicate_username(client):
    client.post('/auth/register', json={
        "user_name": "unique_user",
        "password": "password123"
    })
    res = client.post('/auth/register', json={
        "user_name": "unique_user",
        "password": "password456"
    })
    assert res.status_code == 409


def test_login_success(client):
    client.post('/auth/register', json={
        "user_name": "login_user",
        "password": "validPassword123"
    })

    res = client.post('/auth/login', json={
        "user_name": "login_user",
        "password": "validPassword123"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "token" in data
    assert data["user"]["user_name"] == "login_user"


def test_login_invalid_credentials(client):
    res = client.post('/auth/login', json={
        "user_name": "non_existent",
        "password": "wrongpassword"
    })
    assert res.status_code == 401


def test_me_endpoint_with_valid_token(client):
    reg_res = client.post('/auth/register', json={
        "user_name": "profile_user",
        "password": "mypassword123"
    })
    token = reg_res.get_json()["token"]

    res = client.get('/auth/me', headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.get_json()["user_name"] == "profile_user"


def test_me_endpoint_unauthorized(client):
    res = client.get('/auth/me')
    assert res.status_code == 401
