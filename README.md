### Using the starter project
Step 1
python3 -m venv venv

Step 2
source venv/bin/activate (linux)


# Bee Challenger V2 — Data Pipeline (Airflow + Databricks + dbt)

Este repositório contém uma pipeline de dados com:
- **Apache Airflow** (orquestração)
- **PostgreSQL** (metadata database do Airflow)
- **dbt** (transformações Bronze → Silver → Gold)
- **Databricks** (execução do notebook de ingestão + destino das tabelas via Unity Catalog)

> Padrão de arquitetura: **ELT** com **Medallion Architecture** (Bronze/Silver/Gold).
> 

---

## Arquitetura do Projeto

![Arquitetura utilizada](portainer/imagem.png)

A arquitetura foi definida priorizando **modularidade** e **flexibilidade**, permitindo que as etapas de ingestão e transformação possam ser substituídas por outras plataformas com baixo impacto operacional e reduzido esforço de adaptação.

### Ingestão de Dados

A ingestão é realizada por meio de **notebooks no Databricks**, responsáveis por:

* Consumir os dados da **Open Brewery API**
* Executar a **paginação** das requisições
* Persistir os dados brutos no **Databricks Delta Lakehouse**
* Armazenar os dados em **tabelas gerenciadas**, possibilitando escalabilidade conforme a necessidade do volume de dados

Essa abordagem garante rastreabilidade dos dados brutos e suporte a crescimento do ambiente.

### Transformação de Dados

A camada de transformação é executada utilizando **dbt Cloud**, conectado ao ambiente do Databricks.

O dbt é responsável por:

* Aplicar regras de transformação
* Estruturar as camadas do modelo (ex: Bronze, Silver e Gold)
* Garantir versionamento das transformações
* Facilitar testes e documentação dos modelos

Essa separação entre ingestão e transformação reforça o desacoplamento da arquitetura e melhora a governança dos dados.

---

Essa solução permite construir um **Data Lake escalável, resiliente e orientado a boas práticas modernas de engenharia de dados**.


### Visão geral (componentes)

flowchart LR
  subgraph Local["Ambiente Local (Docker / WSL)"]
    AWeb["Airflow Webserver"]
    ASch["Airflow Scheduler"]
    APg["Postgres (Airflow metadata)"]
    DBT["dbt CLI (dentro do container Airflow)"]
  end

  subgraph Databricks["Databricks (Cloud)"]
    DJ["Databricks Job (Notebook Ingestion)"]
    UC["Unity Catalog<br/>catalog: workspace<br/>schema: dbt_beer"]
    WH["SQL Warehouse (http_path)"]
  end

  AWeb <--> APg
  ASch <--> APg
  ASch --> DJ
  DBT --> WH
  WH --> UC
  DJ --> UC

### Estrutura de pasta

Bee_Challenger_V2/
├─ airflow/
│  ├─ dags/                     # DAGs do Airflow
│  │  └─ beer_pipeline_databricks_dbt.py
│  ├─ logs/                     # logs Airflow (montado em volume)
│  └─ plugins/                  # plugins Airflow (se necessário)
├─ dbt/
│  ├─ dbt_project.yml
│  ├─ packages.yml
│  ├─ models/
│  │  ├─ 1_Bronze/
│  │  ├─ 2_Silver/
│  │  └─ 3_Gold/
│  └─ README.md                 # opcional: doc do dbt
├─ docker-compose.yml
├─ Dockerfile
└─ README.md

## Pre Requisitos
Docker + Docker Compose
WSL2 (no Windows) e integração com Docker Desktop

Acesso ao Databricks:
Workspace URL (Host)
SQL Warehouse HTTP Path
Token (PAT)

Permissões no Unity Catalog:
USE CATALOG workspace
USE SCHEMA dbt_beer
permissão de CREATE/MODIFY no schema para criar tabelas/views

### Configuração (Airflow + dbt + Databricks)

Subindo o ambiente
docker compose up -d --force-recreate

docker ps

Acesse o Airflow:

UI: http://localhost:8080

usuário/senha: admin/admin



### Criando a Connection databricks_default no Airflow (passo a passo)

A DAG usa databricks_conn_id="databricks_default".

Via UI

Airflow → Admin → Connections

Clique em +

Preencha:

Connection Id: databricks_default

Connection Type: Databricks

Host: https://dbc-...cloud.databricks.com

Password: (opcional) token

Extra:

{"token":"SEU_TOKEN_AQUI"}


em caso de falha de verificacao do aiflow (possivel devido as variaveis de ambiente) recomendo utilzar o dbt cloud e fazer os ajustes de credencias com databricks
importa o projeto no dbt cloud e executar dbt run.

testes serao executados, transormaoes da camada silver e gold implementadas dentro do tabelas gerenciadas no lake house.




### Roadmap (próximos upgrades)

melhorar a subida do ambiente do airflow atualemnte bem custosa e burocratica de configurar procurar usar solucao mais pratica para orquestar.
avaliar metdos de orquestracao em cloud 




