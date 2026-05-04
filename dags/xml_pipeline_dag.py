from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "danish",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="xml_ops_pipeline",
    default_args=default_args,
    description="Run XML PySpark Pipeline",
    schedule="@daily",   # runs daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    run_pipeline = BashOperator(
        task_id="run_xml_pipeline",
        bash_command="""
        cd /home/danish/spark-venv/pyspark/projects/xml_ops &&
        export PYTHONPATH=$(pwd) &&
        spark-submit \
          --packages com.databricks:spark-xml_2.12:0.17.0 \
          jobs/xml_pipeline.py
        """
    )

    run_pipeline
