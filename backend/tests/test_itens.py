import uuid

def test_adicionar_item(client):

    email_unico = f"{uuid.uuid4()}@gmail.com"

    # cria usuário
    usuario = client.post(
        "/users",
        json={
            "nome": "Admin",
            "email": email_unico,
            "senha": "123456",
            "tipo": "admin"
        }
    )

    assert usuario.status_code == 200

    # cria produto
    produto = client.post(
        "/produtos",
        json={
            "nome": "Pizza",
            "preco": 45,
            "estoque": 20,
            "unidade": "UN"
        }
    )

    assert produto.status_code == 200

    produto_id = produto.json()["id"]

    # cria comanda
    comanda = client.post(
        "/comandas",
        json={
            "mesa": 5
        }
    )

    assert comanda.status_code == 200

    comanda_id = comanda.json()["id"]

    # adiciona item
    response = client.post(
        "/itens",
        json={
            "comanda_id": comanda_id,
            "produto_id": produto_id,
            "quantidade": 2
        }
    )

    print(response.json())

    assert response.status_code == 200