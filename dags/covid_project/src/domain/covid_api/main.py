from extract import CovidApiExtract

def el_script(
    date: str,
    api_key: str
    
) -> None:
    extract = CovidApiExtract(date=date, key=api_key)
    daily_covid_csv_data = extract.extract_workflow()