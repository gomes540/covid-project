import json
import logging
from google.cloud import storage
from google.oauth2 import service_account
from covid_project.src.domain.exceptions.commons_exceptions import ServiceAccountException
from covid_project.src.external.gcs.gcs_settings import FileType, FilePath


class GCSLoader:
    def __init__(self, *, project_id: str, csv_data_list: list, credentials: str, date: str) -> None:
        self.project_id = project_id
        self.csv_data_list = csv_data_list
        self.bucket = FilePath.BUCKET.value
        self.filename = FilePath.FILENAME.value
        self.content_type = FileType.CONTENT_TYPE.value
        self.date = date
        self.client = self._build_gcs_client(credentials=credentials)

    def _insert_day_in_filename(self, date: str) -> str:
        filename_without_extension = self.filename[:-4]
        full_filename = f"{filename_without_extension}-on-{date}.csv"
        return full_filename

    def _build_gcs_credentials(self, gcs_service_account: str):
        try:
            credentials_dict = json.loads(gcs_service_account)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict
            )
            return credentials
        except ValueError as error:
            raise ServiceAccountException("Invalid Service Account") from error

    def _build_gcs_client(self, credentials: str):
        credentials = self._build_gcs_credentials(
            gcs_service_account=credentials)
        gcs_client = storage.Client(
            project=self.project_id, credentials=credentials)
        return gcs_client

    def get_filepath(self) -> str:
        filepath = self._insert_day_in_filename(self.date)
        return filepath

    def get_bucket(self) -> str:
        return self.bucket

    def load_data(self) -> None:
        csv_filename = self._insert_day_in_filename(self.date)
        bucket = self.client.bucket(self.bucket)
        blob = bucket.blob(csv_filename)
        blob.upload_from_string(
            data=self.csv_data, content_type=self.content_type)
        logging.info(
            f"Data '{csv_filename}' has been loaded successfully to bucket '{self.bucket}'")
