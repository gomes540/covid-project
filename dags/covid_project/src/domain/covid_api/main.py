from covid_project.src.domain.covid_api.extract import CovidApiExtract
from covid_project.src.external.gcs.loader import GCSLoader


def el_script(
    date: str,
    api_key: str,
    project_id: str,
    gcs_credential: str
) -> None:
    extract = CovidApiExtract(date=date, key=api_key)
    daily_covid_csv_data = extract.extract_workflow()
    loader_to_gcs = GCSLoader(
        project_id=project_id,
        csv_data=daily_covid_csv_data,
        credentials=gcs_credential,
        date=date
    )
    loader_to_gcs.load_data()
