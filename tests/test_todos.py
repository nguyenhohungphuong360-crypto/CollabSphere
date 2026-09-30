def test_create_todo(client):
    res = client.post('/todos/', json={
        "title": "Setup Docker",
        "description": "Create Dockerfile and docker-compose",
        "status": "pending"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Setup Docker"
    assert "id" in data


def test_list_todos(client):
    client.post('/todos/', json={"title": "Task 1", "status": "pending"})
    client.post('/todos/', json={"title": "Task 2", "status": "completed"})

    res = client.get('/todos/')
    assert res.status_code == 200
    todos = res.get_json()
    assert len(todos) >= 2


def test_get_todo_by_id(client):
    create_res = client.post('/todos/', json={"title": "Find Me", "status": "pending"})
    todo_id = create_res.get_json()["id"]

    res = client.get(f'/todos/{todo_id}')
    assert res.status_code == 200
    assert res.get_json()["title"] == "Find Me"


def test_get_todo_not_found(client):
    res = client.get('/todos/999999')
    assert res.status_code == 404


def test_update_todo(client):
    create_res = client.post('/todos/', json={"title": "Old Title", "status": "pending"})
    todo_id = create_res.get_json()["id"]

    res = client.put(f'/todos/{todo_id}', json={"title": "New Title", "status": "done"})
    assert res.status_code == 200
    assert res.get_json()["title"] == "New Title"
    assert res.get_json()["status"] == "done"


def test_delete_todo(client):
    create_res = client.post('/todos/', json={"title": "Delete Me", "status": "pending"})
    todo_id = create_res.get_json()["id"]

    res = client.delete(f'/todos/{todo_id}')
    assert res.status_code == 204

    # Verify deleted
    get_res = client.get(f'/todos/{todo_id}')
    assert get_res.status_code == 404
