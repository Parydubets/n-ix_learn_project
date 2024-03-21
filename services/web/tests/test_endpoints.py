import pytest

def test_request_films_200(client):
    response = client.get("/api/v1.0/films")
    assert response.status_code == 200

def test_halo(client):
    response = client.get("/halo")
    assert response.status_code == 200

def test_haloo(client):
    response = client.get("/haloo")
    assert response.status_code == 200

@pytest.mark.filterwarnings("ignore:RemovedInMarshmallow4Warning")
@pytest.mark.filterwarnings("ignore: DeprecationWarning")
def test_films(client):
    assert client.get("/api/v1.0/films").status_code == 200
    assert client.get("/api/v1.0/films?page=2").status_code == 200
    assert client.get("/api/v1.0/films?pag=2").status_code == 400
    assert client.get("/api/v1.0/films?genre=adventure").status_code == 200
    assert client.get("/api/v1.0/films?director=Christopher+Nolan").status_code == 200
    assert client.get("/api/v1.0/films?director=Christopherrr+Nolan").status_code == 400


@pytest.mark.filterwarnings("ignore:RemovedInMarshmallow4Warning")
@pytest.mark.filterwarnings("ignore: DeprecationWarning")
def test_film_2(client):
    assert client.get("/api/v1.0/films?sort=date").status_code == 200
    assert client.get("/api/v1.0/films?sort=r-date").status_code == 200
    assert client.get("/api/v1.0/films?sort=rating").status_code == 200
    assert client.get("/api/v1.0/films?sort=r-rating").status_code == 200
    assert client.get("/api/v1.0/films?sorte=r-rating").status_code == 400
    assert client.get("/api/v1.0/films?sort=r-ratng").status_code == 400
    assert client.get("/api/v1.0/films?date_from=2020-02-03").status_code == 200
    assert client.get("/api/v1.0/films?date_from=2020-02-33").status_code == 400
    assert client.get("/api/v1.0/films?date_from=2024-08-30").status_code == 400
    assert client.get("/api/v1.0/films?date_from=2024-38-30").status_code == 400
    assert client.get("/api/v1.0/films?date_to=2020-02-03").status_code == 200
    assert client.get("/api/v1.0/films?date_to=2020-02-33").status_code == 400
    assert client.get("/api/v1.0/films?date_to=2024-08-30").status_code == 200
    assert client.get("/api/v1.0/films?date_to=2024-38-30").status_code == 400
    assert client.get("/api/v1.0/films?date_from=2025-02-02&date_to=2024-10-30").status_code == 400
