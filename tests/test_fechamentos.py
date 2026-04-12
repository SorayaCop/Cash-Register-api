def test_fechamento_sucesso(client):
    client.post("/api/v1/movimentacoes", json={
        "tipo": "entrada",
        "valor": 100,
        "forma_pagamento": "dinheiro"
    })

    response = client.post("/api/v1/fechamentos", json={
        "saldo_informado": 100,
        "data_inicio": "2024-01-01",
        "data_fim": "2030-01-01"
    })

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["data"]["diferenca"] == 0


def test_fechamento_sem_periodo(client):
    response = client.post("/api/v1/fechamentos", json={
        "saldo_informado": 100
    })

    assert response.status_code == 400