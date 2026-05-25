def test_login(client):

    response = client.post(
        "/login",
        json={
            "email": "gabriel@gmail.com",
            "senha": "123456"
        }
    )

    assert response.status_code == 200