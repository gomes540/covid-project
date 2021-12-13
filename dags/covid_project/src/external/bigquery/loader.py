import json
import logging
import ast
from google.oauth2 import service_account
from google.cloud import bigquery
from datetime import datetime
from covid_project.src.domain.exceptions.commons_exceptions import (
    ServiceAccountException,
)
from covid_project.src.external.bigquery.bq_settings import BQSettings
from covid_project.src.external.bigquery.schema import COVID_RAW_DATA_SCHEMA


class BigqueryLoader:
    def __init__(
        self, *, project_id: str, credentials: str, gcs_files_uri: str
    ) -> None:
        self.project_id = project_id
        self.dataset = BQSettings.DATASET.value
        self.table = BQSettings.TABLE.value
        self.client = self._build_client(credentials)
        self.gcs_files_uri = self._string_to_list(gcs_files_uri)

    def _string_to_list(self, string_list: str):
        list_file_uri = ast.literal_eval(string_list)
        return list_file_uri

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
            project=self.project_id,
        )
        return client

    def _build_job_config(self):
        job_config = bigquery.LoadJobConfig(
            create_disposition="CREATE_IF_NEEDED",
            time_partitioning=bigquery.table.TimePartitioning(field="date"),
            schema=COVID_RAW_DATA_SCHEMA,
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE",
        )
        return job_config

    def _build_table_destination(self) -> str:
        table_id = f"{self.project_id}.{self.dataset}.{self.table}"
        return table_id

    def _build_table_destination_with_partition(
        self, *, table_id: str, partition: str
    ) -> str:
        partitioned_table_id = f"{table_id}${partition}"
        return partitioned_table_id

    def _get_date_from_gcs_uri(self, gcs_uri: str) -> str:
        day = gcs_uri.split(".")[0][-10:]
        partition = datetime.strptime(day, "%Y-%m-%d").strftime("%Y%m%d")
        return partition

    def load_data(self) -> None:
        table_id = self._build_table_destination()
        for file_uri in self.gcs_files_uri:
            partition = self._get_date_from_gcs_uri(file_uri)
            partitioned_table_id = self._build_table_destination_with_partition(
                table_id=table_id, partition=partition
            )
            job_config = self._build_job_config()
            job = self.client.load_table_from_uri(
                source_uris=file_uri,
                destination=partitioned_table_id,
                job_config=job_config,
            )
            job.result()
            logging.info(
                f"csv: '{file_uri}' has beed loaded to table '{partitioned_table_id}' successfully"
            )
