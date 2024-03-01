def test_request_films_200(client):
    response = client.get("/api/web")
    assert response.status_code == 200
    assert b"web" in response.data


def test_request_example(client):
    response = client.get("/api/web")
    assert b"web" in response.data