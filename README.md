# Cash Register API

API REST para controle de movimentações financeiras, fechamento de caixa e geração de resumo financeiro por período.

---

## 📦 Tecnologias

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- Pytest

---

## 📂 Estrutura

app/
├── models/
├── routes/
├── services/
├── config.py
├── errors.py
├── extensions.py
└── init.py

tests/
migrations/
run.py
requirements.txt


---

## ⚙️ Setup

### Clonar repositório

git clone https://github.com/SorayaCop/Cash-Register-api.git
cd Cash-Register-api

Criar ambiente virtual
python -m venv venv

Ativar:

Windows

venv\Scripts\activate

Linux/Mac

source venv/bin/activate
Instalar dependências
pip install -r requirements.txt
Configurar ambiente

Criar .env:

FLASK_DEBUG=True
SECRET_KEY=change-this-secret-key
DATABASE_URL=sqlite:///database.db
Rodar migrations
$env:FLASK_APP="run.py"
flask db upgrade
Executar API
python run.py
🔗 Base URL
http://127.0.0.1:5000
🩺 Health Check
GET /health
💰 Movimentações
Criar movimentação
POST /api/v1/movimentacoes
{
  "tipo": "entrada",
  "valor": 100,
  "forma_pagamento": "dinheiro",
  "descricao": "Suprimento"
}
Listar movimentações
GET /api/v1/movimentacoes

Filtros opcionais:

?data_inicio=YYYY-MM-DD
&data_fim=YYYY-MM-DD
🧾 Fechamento de Caixa
Criar fechamento
POST /api/v1/fechamentos
{
  "saldo_informado": 150,
  "data_inicio": "2024-01-01",
  "data_fim": "2030-01-01"
}
Listar fechamentos
GET /api/v1/fechamentos
📊 Resumo Financeiro
GET /api/v1/resumo

Exemplo:

/api/v1/resumo?data_inicio=2024-01-01&data_fim=2030-01-01
🔄 Padrão de Resposta
Sucesso
{
  "success": true,
  "message": "Operação realizada com sucesso",
  "data": {}
}
Erro
{
  "success": false,
  "error": {
    "code": "invalid_value",
    "message": "Valor inválido"
  }
}
🧪 Testes
pytest

---

