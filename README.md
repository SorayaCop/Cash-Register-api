# Cash Register API

API REST para controle de movimentações financeiras e fechamento de caixa, com validação de dados, regras de negócio, testes automatizados e histórico persistente.

Este projeto foi desenvolvido com o objetivo de demonstrar habilidades reais de desenvolvimento backend com Flask, indo além de um CRUD simples.

---

## 📌 Visão Geral

A API simula o funcionamento de um sistema de caixa:

- registro de entradas e saídas financeiras
- filtragem por período
- cálculo de fechamento de caixa
- comparação entre saldo esperado e informado
- resumo financeiro por forma de pagamento

---

## 🚀 Funcionalidades

- API versionada (`/api/v1`)
- Cadastro de movimentações (entrada/saída)
- Listagem com filtros por data
- Fechamento de caixa por período
- Resumo financeiro por intervalo de datas
- Validação de dados de entrada
- Tratamento padronizado de erros
- Precisão financeira com `Decimal`
- Migrations com Flask-Migrate
- Testes automatizados com Pytest

---

## 🛠️ Tecnologias

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- Pytest

---

## 📂 Estrutura do Projeto
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

## 🧠 Arquitetura

O projeto segue separação de responsabilidades:

- **routes** → camada HTTP (entrada/saída)
- **services** → regras de negócio
- **models** → persistência
- **errors** → padronização de respostas
- **tests** → validação automatizada

---

## 💰 Regras de Negócio

### Movimentação

Campos obrigatórios:

- `tipo`: `entrada` ou `saida`
- `valor`: número positivo
- `forma_pagamento`: obrigatório
- `descricao`: opcional

---

### Fechamento de Caixa

Requer:

- `saldo_informado`
- `data_inicio`
- `data_fim`

Calcula:

- total de entradas
- total de saídas
- saldo esperado
- diferença
- resumo por forma de pagamento

---

### Resumo Financeiro

Retorna:

- período analisado
- total de entradas
- total de saídas
- saldo final
- agrupamento por forma de pagamento

---

## 📦 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/SorayaCop/Cash-Register-api.git
cd Cash-Register-api


