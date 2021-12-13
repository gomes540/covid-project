from covid_project.src.domain.covid_api.extract import CovidApiExtract
from covid_project.src.external.gcs.loader import GCSLoader
from covid_project.src.external.bigquery.loader import BigqueryLoader


def extract_and_load__to_gcs(
    start_date: str,
    end_date: str,
    api_key: str,
    project_id: str,
    gcs_credential: str
) -> list:
    api_extract = CovidApiExtract(
        start_date=start_date,
        end_date=end_date,
        key=api_key
    )
    daily_covid_csv_data_dict = api_extract.extract_workflow()
    loader_to_gcs = GCSLoader(
        project_id=project_id,
        csv_data_dict=daily_covid_csv_data_dict,
        credentials=gcs_credential
    )
    gcs_uri_list = loader_to_gcs.load_data()
    return gcs_uri_list


def gcs_csv_file_to_bigquery(
    project_id: str,
    gcs_credential: str,
    gcs_files_uri: str,
) -> None:
    loader_to_bq = BigqueryLoader(
        project_id=project_id,
        credentials=gcs_credential,
        gcs_files_uri=gcs_files_uri,
    )
    loader_to_bq.load_data()
