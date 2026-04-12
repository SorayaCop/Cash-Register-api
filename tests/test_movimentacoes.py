def test_criar_movimentacao_sucesso(client):
    response = client.post("/api/v1/movimentacoes", json={
        "tipo": "entrada",
        "valor": 100,
        "forma_pagamento": "dinheiro",
        "descricao": "teste"
    })

    assert response.status_code == 201

    data = response.get_json()

    assert data["success"] is True
    assert float(data["data"]["valor"]) == 100.0
    assert data["data"]["tipo"] == "entrada"


def test_criar_movimentacao_sem_body(client):
    response = client.post("/api/v1/movimentacoes")

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["error"]["code"] == "missing_body"


def test_criar_movimentacao_valor_invalido(client):
    response = client.post("/api/v1/movimentacoes", json={
        "tipo": "entrada",
        "valor": "abc",
        "forma_pagamento": "pix"
    })

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["error"]["code"] == "invalid_value"


def test_listar_movimentacoes(client):
    client.post("/api/v1/movimentacoes", json={
        "tipo": "entrada",
        "valor": 50,
        "forma_pagamento": "pix"
    })

    response = client.get("/api/v1/movimentacoes")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert len(data["data"]) == 1
    assert float(data["data"][0]["valor"]) == 50.0