import json
from google.oauth2 import service_account
from google.cloud import bigquery
from covid_project.src.domain.exceptions.commons_exceptions import ServiceAccountException
from covid_project.src.models.bigquery_cte import BQInfo

class BigqueryLoader:
    def __init__(self, *, project_id: str, bq_credentials: str) -> None:
        self.project_id = project_id
        self.bq_credentials = bq_credentials
        self.dataset = BQInfo.DATATSET,
        self.table =  BQInfo.TABLE,
        self.client = self._build_client()
        
    def _build_bigquery_credentials(self, service_account_json: str):
        try:
            credentials_dict = json.loads(service_account_json)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict
            )
            return credentials
        except ValueError as error:
            raise ServiceAccountException("Invalid Service Account") from error
    
    def _build_client(self):
        