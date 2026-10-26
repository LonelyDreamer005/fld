
from app import app


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_get_students():
    client = app.test_client()
    response = client.get("/students")
    assert response.status_code == 200
