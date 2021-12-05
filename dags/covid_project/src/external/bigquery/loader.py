import json
from google.oauth2 import service_account
from google.cloud import bigquery
from datetime import datetime
from covid_project.src.domain.exceptions.commons_exceptions import ServiceAccountException
from covid_project.src.external.bigquery.bq_settings import BQSettings
from covid_project.src.external.bigquery.schema import COVID_RAW_DATA_SCHEMA


class BigqueryLoader:
    def __init__(self, *, project_id: str, credentials: str, gcs_filepath: str, bucket_name: str) -> None:
        self.project_id = project_id
        self.dataset = BQSettings.DATASET.value
        self.table = BQSettings.TABLE.value
        self.client = self._build_client(credentials)
        self.gcs_filepath = gcs_filepath
        self.bucket_name = bucket_name

    def _build_bigquery_credentials(self, service_account_json: str):
        try:
            credentials_dict = json.loads(service_account_json)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict
            )
            return credentials
        except ValueError as error:
            raise ServiceAccountException("Invalid Service Account") from error

    def _build_client(self, credentials: str):
        client = bigquery.Client(
            credentials=self._build_bigquery_credentials(credentials),
            project=self.project_id
        )
        return client

    def _build_job_config(self):
        job_config = bigquery.LoadJobConfig(
            create_disposition="CREATE_IF_NEEDED",
            time_partitioning=bigquery.table.TimePartitioning(field="date"),
            schema=COVID_RAW_DATA_SCHEMA,
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE"
        )
        return job_config

    def _build_table_destination(self) -> str:
        table_id = f"{self.project_id}.{self.dataset}.{self.table}"
        return table_id

    def _convert_data_format(self, date: str) -> str:
        converted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")
        return converted_date

    def _build_table_destination_with_partition(self, *, table_id: str, date: str) -> str:
        converted_date = self._convert_data_format(date=date)
        partitioned_table_id = f"{table_id}${converted_date}"
        return partitioned_table_id

    def _build_gcs_source_uri(self) -> str:
        source_uri = f"gs://{self.bucket_name}/{self.gcs_filepath}"
        return source_uri

    def load_data(self, *, date: str) -> None:
        table_id = self._build_table_destination()
        source_uri = self._build_gcs_source_uri()
        partitioned_table_id = self._build_table_destination_with_partition(
            table_id=table_id,
            date=date
        )
        job_config = self._build_job_config()
        job = self.client.load_table_from_uri(
            source_uris=source_uri,
            destination=partitioned_table_id,
            job_config=job_config
        )
        job.result()
