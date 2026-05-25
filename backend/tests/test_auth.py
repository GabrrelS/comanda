from .conftest import client


def test_login():
    response = client.post(
        "/login",
        json={
            "email": "admin@email.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200


def test_login_invalido():
    response = client.post(
        "/login",
        json={
            "email": "errado@email.com",
            "password": "senha_errada"
        }
    )

    assert response.status_code == 401