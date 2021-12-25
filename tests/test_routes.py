
def test_cli(runner):
    result = runner.invoke(args=['init-db'])
    assert 'Initialized the database.' in result.output


def test_home_page(client):

    response = client.get('/')
    assert response.status_code == 200


def test_students(client):
    rv = client.get("/students/")
    assert rv.status_code == 200


def test_groups(client):
    rv = client.get("/groups/")
    assert rv.status_code == 200


def test_student(client):
    rv = client.get("/students/1")
    assert rv.status_code == 200


def test_error(client):
    rv = client.get("/student")
    assert rv.status_code == 404


def test_api_get_all(client):
    rv = client.get("/api/v1/students/")
    assert rv.status_code == 200


def test_api_get_by_id(client):
    rv = client.get("/api/v1/students/1")
    json_data = rv.get_json()
    assert json_data['id'] == 1


def test_api_post_new_student(client):
    rv = client.post("/api/v1/students/", json={'first_name': 'Jon', 'last_name': 'Snow'})
    json_data = rv.json
    assert json_data['first_name'] == 'Jon'
    assert json_data['last_name'] == 'Snow'
    assert json_data['courses'] == []


def test_process_course_add(client):
    rv1 = client.get('/_update_courses/',
                     data={'course': 'Law', 'student_id': '201', 'action': "append"})
    assert rv1.status_code == 200
    rv2 = client.get("/api/v1/students/201")
    assert 'Law' in rv2.get_json()['courses']


def test_process_course_remove(client):
    rv1 = client.get('/_update_courses/',
                     data={'course': 'Law', 'student_id': '201', 'action': "remove"})
    assert rv1.status_code == 200
    rv2 = client.get("/api/v1/students/201")
    assert 'Law' not in rv2.get_json()['courses']


def test_delete_student(client):
    rv1 = client.get('/_delete_student/',
                     data={'student_id': 201})
    assert rv1.status_code == 200
    rv2 = client.get("/api/v1/students/201")
    assert rv2.status_code == 404
