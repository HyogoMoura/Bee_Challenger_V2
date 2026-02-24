from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import datetime

DBT_DIR = "/opt/airflow/dbt"

with DAG(
    dag_id="beer_pipeline_databricks_dbt",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ingestion", "databricks", "dbt", "medallion"],
) as dag:

    # 1) Executa o Job do Databricks que roda o notebook de ingestão
    run_ingestion_notebook = DatabricksRunNowOperator(
        task_id="run_ingestion_notebook",
        databricks_conn_id="databricks_default",
        job_id=1022077442808787,  
    )

    # 2) dbt deps
    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command=f"cd {DBT_DIR} && dbt deps --project-dir {DBT_DIR}",
    )

    # 3) Bronze/Silver/Gold por namespace (confirmado pelo seu dbt ls)
    dbt_bronze = BashOperator(
        task_id="dbt_bronze",
        bash_command=f"cd {DBT_DIR} && dbt run --project-dir {DBT_DIR} --select my_new_project.1_Bronze -v",
    )

    dbt_silver = BashOperator(
        task_id="dbt_silver",
        bash_command=f"cd {DBT_DIR} && dbt run --project-dir {DBT_DIR} --select my_new_project.2_Silver -v",
    )

    dbt_gold = BashOperator(
        task_id="dbt_gold",
        bash_command=f"cd {DBT_DIR} && dbt run --project-dir {DBT_DIR} --select my_new_project.3_Gold -v",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && dbt test --project-dir {DBT_DIR} -v",
        trigger_rule=TriggerRule.ALL_DONE, 
    )

    run_ingestion_notebook >> dbt_deps >> dbt_bronze >> dbt_silver >> dbt_gold >> dbt_test