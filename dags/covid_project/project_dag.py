from airflow import DAG
from datetime import datetime
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from covid_project.src.domain.covid_api.main import (
    extract_and_load_to_gcs,
    gcs_csv_file_to_bigquery,
)


start_date = '{{ yesterday_ds if dag_run.conf.get("start_date") == None else dag_run.conf.get("start_date") }}'
end_date = '{{ yesterday_ds if dag_run.conf.get("end_date") == None else dag_run.conf.get("end_date") }}'

default_args = {
    "owner": "Felipe Gomes",
    "start_date": datetime(2021, 1, 1),
    "depends_on_past": False,
}

with DAG(
    dag_id="elt_covid_project",
    default_args=default_args,
    catchup=False,
    schedule_interval="30 4 * * *",
    description="Extract data from COVID API, save in GCS and load to Bigquery",
    tags=["covid_project"],
) as dag:
    start = DummyOperator(task_id="start")

    end = DummyOperator(task_id="end")

    extract_and_load_to_gcs = PythonOperator(
        task_id="covid_extract_and_load_to_gcs",
        python_callable=extract_and_load_to_gcs,
        provide_context=True,
        op_kwargs={
            "start_date": start_date,
            "end_date": end_date,
            "api_key": Variable.get("covid_api_key"),
            "project_id": Variable.get("project_id"),
            "covid_project_service_account": Variable.get(
                "covid_project_service_account_secret"
            ),
        },
    )

    gcs_files_uri = "{{ task_instance.xcom_pull(task_ids='covid_extract_and_load_to_gcs', dag_id='elt_covid_project', key='return_value') }}"

    raw_gcs_csv_file_to_bigquery = PythonOperator(
        task_id="covid_raw_gcs_csv_file_to_bigquery",
        python_callable=gcs_csv_file_to_bigquery,
        provide_context=True,
        op_kwargs={
            "gcs_files_uri": gcs_files_uri,
            "project_id": Variable.get("project_id"),
            "covid_project_service_account": Variable.get(
                "covid_project_service_account_secret"
            ),
        },
    )

    start >> extract_and_load_to_gcs >> raw_gcs_csv_file_to_bigquery >> end
