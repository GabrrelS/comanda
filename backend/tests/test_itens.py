from .conftest import client


def test_adicionar_item():

    # LOGIN
    login = client.post(
        "/login",
        json={
            "email": "admin@email.com",
            "password": "123456"
        }
    )

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # TESTE DA ROTA
    response = client.post(
        "/itens",
        headers=headers,
        json={
            "comanda_id": 1,
            "produto_id": 1,
            "quantidade": 2
        }
    )

    assert response.status_code == 200