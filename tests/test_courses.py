def test_create_course(client):
    res = client.post('/courses/', json={
        "course_name": "Software Architecture 101",
        "description": "Learn clean architecture and patterns",
        "status": "active"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["course_name"] == "Software Architecture 101"
    assert "id" in data


def test_list_courses(client):
    res = client.get('/courses/')
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_get_course_by_id(client):
    create_res = client.post('/courses/', json={
        "course_name": "Design Patterns",
        "status": "active"
    })
    course_id = create_res.get_json()["id"]

    res = client.get(f'/courses/{course_id}')
    assert res.status_code == 200
    assert res.get_json()["course_name"] == "Design Patterns"


def test_update_course(client):
    create_res = client.post('/courses/', json={
        "course_name": "Course To Update",
        "status": "draft"
    })
    course_id = create_res.get_json()["id"]

    res = client.put(f'/courses/{course_id}', json={
        "course_name": "Updated Course Name",
        "status": "published"
    })
    assert res.status_code == 200
    assert res.get_json()["course_name"] == "Updated Course Name"
    assert res.get_json()["status"] == "published"


def test_delete_course(client):
    create_res = client.post('/courses/', json={
        "course_name": "Course To Delete",
        "status": "archived"
    })
    course_id = create_res.get_json()["id"]

    res = client.delete(f'/courses/{course_id}')
    assert res.status_code == 204

    get_res = client.get(f'/courses/{course_id}')
    assert get_res.status_code == 404
