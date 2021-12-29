
def test_cli(runner):
    result = runner.invoke(args=['init-db'])
    assert 'Database is initialized.' in result.output


def test_api(client):
    rv = client.get("/")
    assert rv.status_code == 200


def test_api_info(client):
    rv = client.get("api/info")
    assert rv.status_code == 200


def test_api_info_data(client):
    rv = client.get("api/info")
    assert 'startDate' in rv.get_json()[0]
    assert 'endDate' in rv.get_json()[1]
    assert 'Type' in rv.get_json()[2]
    assert 'Grouping' in rv.get_json()[3]
    assert 'Filters' in rv.get_json()[4]


def test_api_timeline_path(client):
    rv = client.get("/api/timeline", json={'startDate': '2018-01-01',
                                           'endDate': '2020-01-01'})
    assert rv.status_code == 200


def test_api_timeline(client):
    rv = client.get("/api/timeline", json={'startDate': '2018-01-01',
                                           'endDate': '2020-01-01'})
    assert 'timeline' in rv.get_json()


def test_api_timeline_cumulative(client):
    rv = client.get("/api/timeline", json={'startDate': '2018-01-01',
                                           'endDate': '2020-01-01',
                                           'Type': 'cumulative'})
    result = rv.get_json()['timeline']
    assert (result[0]['value'] + result[1]['value']) < result[2]['value']
