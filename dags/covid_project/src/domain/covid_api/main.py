from covid_project.src.domain.covid_api.extract import CovidApiExtract
from covid_project.src.external.gcs.loader import GCSLoader
from covid_project.src.external.bigquery.loader import BigqueryLoader


def el_script(
    date: str,
    api_key: str,
    project_id: str,
    gcs_credential: str
) -> None:
    api_extract = CovidApiExtract(date=date, key=api_key)
    daily_covid_csv_data = api_extract.extract_workflow()
    loader_to_gcs = GCSLoader(
        project_id=project_id,
        csv_data=daily_covid_csv_data,
        credentials=gcs_credential,
        date=date
    )
    gcs_filepath = loader_to_gcs.get_filepath()
    bucket_name = loader_to_gcs.get_bucket()
    loader_to_gcs.load_data()
    loader_to_bq = BigqueryLoader(
        project_id=project_id,
        credentials=gcs_credential,
        gcs_filepath=gcs_filepath,
        bucket_name=bucket_name
    )
    loader_to_bq.load_data(date=date)
