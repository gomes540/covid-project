import json
import logging
from google.cloud import storage
from google.oauth2 import service_account
from covid_project.src.domain.exceptions.commons_exceptions import ServiceAccountException
from covid_project.src.external.gcs.gcs_settings import FileType, FilePath


class GCSLoader:
    def __init__(self, *, project_id: str, csv_data_dict: dict, credentials: str) -> None:
        self.project_id = project_id
        self.csv_data_dict = csv_data_dict
        self.bucket = FilePath.BUCKET.value
        self.filename = FilePath.FILENAME.value
        self.content_type = FileType.CONTENT_TYPE.value
        self.client = self._build_gcs_client(credentials=credentials)

    def _insert_day_in_filename_as_dict_keys(self, csv_dict: dict) -> str:
        filename_without_extension = self.filename[:-4]
        full_csv_data_dict = {
            f"{filename_without_extension}-on-{day}.csv": daily_csv_data for (day, daily_csv_data) in csv_dict.items()}
        return full_csv_data_dict

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

    def get_bucket(self) -> str:
        return self.bucket

    def load_data(self) -> list:
        gcs_uri_list = []
        filename_and_data_dict = self._insert_day_in_filename_as_dict_keys(
            self.csv_data_dict)
        bucket = self.client.bucket(self.bucket)
        for filename, daily_data in filename_and_data_dict.items():
            blob = bucket.blob(filename)
            blob.upload_from_string(
                data=daily_data, content_type=self.content_type)
            logging.info(
                f"Data '{filename}' has been loaded successfully to bucket '{self.bucket}'")
            gcs_uri_list.append(f'gs://{self.bucket}/{filename}')
        print(gcs_uri_list)
        return gcs_uri_list
