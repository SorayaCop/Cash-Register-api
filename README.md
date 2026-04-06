# Cash Register API

API REST para controle de movimentações financeiras e fechamento de caixa.

Este projeto simula um fluxo real de operação de caixa, permitindo registrar entradas e saídas, calcular o saldo esperado e comparar com o saldo informado no fechamento.

---

## 📌 Funcionalidades

* Registrar movimentações (entrada e saída)
* Listar movimentações
* Calcular fechamento de caixa
* Registrar histórico de fechamentos
* Listar fechamentos realizados

---

## 🧠 Regra de negócio

O sistema:

* armazena movimentações financeiras
* calcula automaticamente:

  * total de entradas
  * total de saídas
  * saldo esperado
* compara com o saldo informado
* retorna a diferença
* registra o fechamento no banco

---

## 🚀 Tecnologias

* Python
* Flask
* SQLAlchemy
* SQLite

---

## ▶️ Como executar

### 1. Clonar o repositório

```bash
git clone <seu-repo>
cd cash-register-api
```

---

### 2. Criar ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Criar banco de dados

```bash
python
```

```python
from app import create_app
from app.extensions import db
from app.models.movimentacao import Movimentacao
from app.models.fechamento import Fechamento

app = create_app()

with app.app_context():
    db.create_all()
```

---

### 5. Rodar a aplicação

```bash
python run.py
```

---

## 📡 Endpoints

### 🔹 Movimentações

#### Criar movimentação

`POST /movimentacoes`

```json
{
  "tipo": "entrada",
  "valor": 100,
  "forma_pagamento": "dinheiro"
}
```

---

#### Listar movimentações

`GET /movimentacoes`

---

### 🔹 Fechamento

#### Realizar fechamento

`POST /fechamentos`

```json
{
  "saldo_informado": 80
}
```

---

#### Listar fechamentos

`GET /fechamentos`

---

## 📁 Estrutura

```
app/
 ├── routes/
 ├── services/
 ├── models/
 ├── extensions.py
 └── __init__.py
```

---

## 🎯 Objetivo

Este projeto foi desenvolvido para praticar:

* construção de APIs REST
* separação de responsabilidades (routes, services, models)
* persistência de dados
* implementação de regras de negócio

---

## 💡 Próximos passos

* adicionar timestamps
* resumo por forma de pagamento
* filtros por período
* testes automatizados
