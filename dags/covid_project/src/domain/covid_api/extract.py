import requests
import pandas as pd
import logging
from covid_project.src.domain.covid_api.api_extract_settings import ApiConstants, RequestMethod


class CovidApiExtract:
    def __init__(self, *, start_date: str, end_date: str, key: str) -> None:
        self.url = ApiConstants.URL.value
        self.host = ApiConstants.HOST.value
        self.key = key
        self.start_date = start_date
        self.end_date = end_date
        self.querystring_list = self._build_querystring_list()
        self.headers = self._build_headers()

    def _build_day_list(self, *, start_date: str, end_date: str) -> list:
        day_list = pd.date_range(start=start_date, end=end_date).to_list()
        day_list = [day.strftime("%Y-%m-%d") for day in day_list]
        return day_list

    def _build_headers(self) -> dict:
        headers = {
            'x-rapidapi-host': self.host,
            'x-rapidapi-key': self.key
        }
        return headers

    def _build_querystring_list(self) -> list:
        day_list = self._build_day_list(
            start_date=self.start_date,
            end_date=self.end_date
        )
        querystring_list = [{'date': day} for day in day_list]
        return querystring_list

    def _make_http_request(self) -> list:
        response_list = []
        try:
            for querystring in self.querystring_list:
                response = requests.request(
                    method=RequestMethod.GET.value,
                    url=self.url,
                    headers=self.headers,
                    params=querystring
                )
                logging.info(
                    f"Extracted the {querystring['date']} data successfully")
                response_list.append(response)
            return response_list
        except requests.exceptions.HTTPError as error:
            raise SystemExit(error)

    def _http_response_to_csv(self, http_response_list: list) -> str:
        api_data_as_csv_list = []
        for http_response in http_response_list:
            response_as_dict = http_response.json()
            api_data = response_as_dict["data"]
            api_data_as_df = pd.json_normalize(api_data)
            api_data_as_csv = api_data_as_df.to_csv(index=False)
            api_data_as_csv_list.append(api_data_as_csv)
        return api_data_as_csv_list

    def _build_dict_from_days_and_response(self, start_date: str, end_date: str, csv_response: list) -> dict:
        day_list = self._build_day_list(
            start_date=start_date,
            end_date=end_date
        )
        mapped_response = dict(zip(day_list, csv_response))
        return mapped_response

    def extract_workflow(self) -> dict:
        covid_api_response_list = self._make_http_request()
        daily_covid_csv_list = self._http_response_to_csv(
            covid_api_response_list)
        mapped_response_and_day = self._build_dict_from_days_and_response(
            start_date=self.start_date,
            end_date=self.end_date,
            csv_response=daily_covid_csv_list
        )
        return mapped_response_and_day
