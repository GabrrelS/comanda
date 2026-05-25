from .conftest import client


def test_criar_comanda():
    response = client.post(
        "/comandas",
        json={
            "cliente": "João",
            "mesa": 5
        }
    )

    assert response.status_code == 200