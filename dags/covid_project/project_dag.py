from airflow import DAG
from datetime import datetime
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from covid_project.src.domain.covid_api.main import el_script


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
) as dag:
    start = DummyOperator(task_id="start")

    end = DummyOperator(task_id="end")

    el_project = PythonOperator(
        task_id="covid_el",
        python_callable=el_script,
        provide_context=True,
        op_kwargs={
            "start_date": start_date,
            "end_date": end_date,
            "api_key": Variable.get("covid_api_key"),
            "project_id": Variable.get("project_id"),
            "gcs_credential": Variable.get("gcs_service_account"),
        }
    )

    start >> el_project >> end
