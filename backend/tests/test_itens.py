def test_adicionar_item(client):
    
    response = client.post(
        "/itens",
        json={
            "comanda_id": 1,
            "produto_id": 1,
            "quantidade": 2
        }
    )

    assert response.status_code == 200