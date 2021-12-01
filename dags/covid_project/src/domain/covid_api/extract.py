import requests
from src.models.api_extract_cte import ApiConstants

class CovidApiExtract:
    def __init__(self, date: str, key: str) -> None:
        self.url = ApiConstants.URL
        self.host = ApiConstants.HOST
        self.key = key
        self.date = date
        self.querystring = self._build_querystring()
        self.headers = self._build_headers()
        
    def _build_headers(self) -> dict:
        headers = {
            'x-rapidapi-host':self.host,
            'x-rapidapi-key': self.key
        }
        return headers
    
    def _build_querystring():
        pass
        
        