def test_request_films_200(client):
    response = client.get("/api/films")
    assert response.status_code == 200
    assert b"films" in response.data


def test_request_example(client):
    response = client.get("/api/films")
    assert b"films" in response.data