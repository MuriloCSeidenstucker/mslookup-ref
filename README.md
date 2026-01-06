# mslookup

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Poetry](https://img.shields.io/badge/dependencies-poetry-blue.svg)
![Architecture](https://img.shields.io/badge/architecture-clean%20architecture-brightgreen.svg)
![Database](https://img.shields.io/badge/database-sqlite-lightgrey.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Linting: Pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
![License](https://img.shields.io/badge/license-MIT-green.svg)

API para consulta de registros de medicamentos da ANVISA a partir de dados públicos.

Este projeto tem como objetivo facilitar a busca e análise de registros de medicamentos, utilizando os dados abertos da ANVISA, com foco em clareza, rastreabilidade e decisões técnicas defensáveis.

## 📌 O que este projeto faz

*   Baixa e processa dados públicos da ANVISA (CSV oficial)
*   Normaliza informações relevantes para busca
*   Armazena os dados localmente em banco de dados
*   Disponibiliza uma API para busca de medicamentos por:
    *   nome do produto
    *   princípio ativo
    *   empresa detentora do registro
*   Aplica regras de negócio baseadas em análise empírica dos dados

## ❗ O que este projeto não faz

*   Não substitui a consulta oficial no site da ANVISA
*   Não garante a situação regulatória final de um medicamento
*   Não realiza validação jurídica ou regulatória

> **A confirmação oficial deve sempre ser feita diretamente no site da ANVISA.**

## 🧠 Decisões técnicas importantes

Durante o desenvolvimento, foi identificado que os dados públicos da ANVISA apresentam inconsistências entre:

*   status do registro (VÁLIDO, ATIVO, INATIVO, CADUCO/CANCELADO)
*   data de vencimento
*   situação apresentada no site oficial da ANVISA

Após análise por amostragem e comparação com o site oficial, foi adotada a seguinte estratégia:

1.  **Status negativos** (INATIVO, CADUCO/CANCELADO) são tratados como sinal forte de invalidez.
2.  **Status positivos** e datas futuras não são tratados como garantia absoluta de validade.
3.  O backend preserva todos os dados, mas expõe ao usuário apenas informações mais confiáveis.

Essa abordagem reduz falsos positivos críticos e mantém transparência sobre as limitações dos dados.

## 🛠 Tecnologias utilizadas

*   Python
*   FastAPI
*   SQLAlchemy
*   SQLite (MVP)
*   Poetry
*   Clean Architecture

## 📦 Criação do schema do banco de dados

Este projeto utiliza SQLAlchemy para gerenciamento do banco de dados. Antes de carregar os dados da ANVISA, é necessário criar as tabelas conforme os modelos definidos no projeto.

Para isso, existe um script responsável por inicializar o schema do banco de dados.

Esse script:

*   Inicializa a conexão com o banco de dados
*   Carrega as entidades mapeadas pelo SQLAlchemy
*   Cria automaticamente todas as tabelas necessárias
*   Garante que o banco esteja pronto para receber os dados processados

A criação das tabelas é feita a partir das entidades definidas no projeto, garantindo que o schema do banco esteja sempre alinhado com o modelo de dados da aplicação.

## ▶️ Como rodar o projeto

### 1. Instalar dependências
```bash
poetry install
```

### 2. Criar automaticamente todas as tabelas necessárias
```bash
poetry run python .\src\infra\db\settings\create_tables.py
```

### 3. Baixar e processar os dados da ANVISA
```bash
poetry run python .\src\ingest\ingest_anvisa.py
```

Isso irá:
*   baixar o CSV oficial
*   processar os dados
*   popular o banco de dados local

### 4. Iniciar a API
```bash
poetry run python .\run.py
```

A API ficará disponível em:
[http://localhost:5000](http://localhost:5000)

A documentação interativa (Swagger) pode ser acessada em:
[http://localhost:5000/docs](http://localhost:5000/docs)

## 🔍 Exemplo de uso

### Requisição
`GET /drugs/search?product_name=metronidazol`

### Exemplo de resposta
```json
{
  "data": {
    "count": 1,
    "attributes": [
      {
        "registration_number": "123456789",
        "product_name": "METRONIDAZOL",
        "active_ingredient": "METRONIDAZOL",
        "registration_holder": "LABORATÓRIO EXEMPLO",
        "expiration_date": "2026-03-01"
      }
    ]
  }
}
```

## ⚠️ Aviso importante

Os dados retornados por esta API são baseados exclusivamente nos dados públicos da ANVISA.

**Antes de qualquer decisão regulatória, comercial ou clínica, confirme sempre as informações diretamente no site oficial da ANVISA.**

## 📄 Licença

Este projeto está licenciado sob os termos da licença MIT.
