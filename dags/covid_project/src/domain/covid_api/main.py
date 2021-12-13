from covid_project.src.domain.covid_api.extract import CovidApiExtract
from covid_project.src.external.gcs.loader import GCSLoader
from covid_project.src.external.bigquery.loader import BigqueryLoader


def extract_and_load_to_gcs(
    start_date: str,
    end_date: str,
    api_key: str,
    project_id: str,
    covid_project_service_account: str,
) -> list:
    api_extract = CovidApiExtract(start_date=start_date, end_date=end_date, key=api_key)
    daily_covid_csv_data_dict = api_extract.extract_workflow()
    loader_to_gcs = GCSLoader(
        project_id=project_id,
        csv_data_dict=daily_covid_csv_data_dict,
        credentials=covid_project_service_account,
    )
    gcs_uri_list = loader_to_gcs.load_data()
    return gcs_uri_list


def gcs_csv_file_to_bigquery(
    project_id: str,
    covid_project_service_account: str,
    gcs_files_uri: str,
) -> None:
    loader_to_bq = BigqueryLoader(
        project_id=project_id,
        credentials=covid_project_service_account,
        gcs_files_uri=gcs_files_uri,
    )
    loader_to_bq.load_data()
