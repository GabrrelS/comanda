def test_criar_comanda(client):
    
    response = client.post(
        "/comandas",
        json={
            "cliente": "João",
            "mesa": 5
        }
    )

    assert response.status_code == 200