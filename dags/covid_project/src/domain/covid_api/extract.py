import requests

class CovidApiExtract:
    def __init__(self, date: str, key: str) -> None:
        self.url = 'https://covid-19-statistics.p.rapidapi.com/reports'
        self.host = 'covid-19-statistics.p.rapidapi.com'
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
        
        