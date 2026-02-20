from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

DBT_DIR = "/opt/airflow/dbt"

with DAG(
    dag_id="dbt_medallion_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["dbt", "databricks", "medallion"],
) as dag:

    deps = BashOperator(
        task_id="dbt_deps",
        bash_command=f"cd {DBT_DIR} && dbt deps --project-dir {DBT_DIR}",
    )

    bronze = BashOperator(
        task_id="bronze",
        bash_command=f"cd {DBT_DIR} && dbt run --project-dir {DBT_DIR} --select my_new_project.1_Bronze -v",
    )

    silver = BashOperator(
        task_id="silver",
        bash_command=f"cd {DBT_DIR} && dbt run --project-dir {DBT_DIR} --select my_new_project.2_Silver -v",
    )

    gold = BashOperator(
        task_id="gold",
        bash_command=f"cd {DBT_DIR} && dbt run --project-dir {DBT_DIR} --select my_new_project.3_Gold -v",
    )

    tests = BashOperator(
        task_id="tests",
        bash_command=f"cd {DBT_DIR} && dbt test --project-dir {DBT_DIR} -v",
    )

    deps >> bronze >> silver >> gold >> tests