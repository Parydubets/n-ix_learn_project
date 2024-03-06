def test_request_films_200(client):
    response = client.get("/api/v1.0/directors")
    assert response.status_code == 200
    assert b"endpoint returns directors list" in response.data

