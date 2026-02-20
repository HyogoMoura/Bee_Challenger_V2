FROM apache/airflow:2.8.1

USER airflow

RUN pip install --no-cache-dir \
    dbt-databricks \
    apache-airflow-providers-databricks

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow

