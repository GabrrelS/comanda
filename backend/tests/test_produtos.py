def test_criar_produto(client):

    response = client.post(
        "/produtos",
        json={
            "nome": "Pizza",
            "preco": 45,
            "estoque": 20,
            "unidade": "UN"
        }
    )

    assert response.status_code == 200