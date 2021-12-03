import json
from google.cloud import storage
from google.cloud.storage import Blob
from google.oauth2 import service_account
from covid_project.src.domain.exceptions.commons_exceptions import ServiceAccountException

class GCSLoader:
    def __init__(self, *, project_id: str, csv_data: str, credentials: str) -> None:
        self.project_id = project_id
        self.csv_data = csv_data
        self.credentials = self._build_gcs_client(credentials=credentials)
        
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
        credentials = self._build_gcs_credentials(gcs_service_account=credentials)
        gcs_client = storage.Client(project=self.project_id, credentials=credentials)
        return gcs_client