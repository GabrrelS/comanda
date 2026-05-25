from .conftest import client


def test_listar_produtos():
    response = client.get("/produtos")

    assert response.status_code == 200


def test_criar_produto():
    response = client.post(
        "/produtos",
        json={
            "nome": "Pizza",
            "preco": 45.0,
            "estoque": 10,
            "unidade": "UN",
            "categoria": "Comida"
        }
    )

    assert response.status_code == 200