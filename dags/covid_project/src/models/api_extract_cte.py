from dataclasses import dataclass

@dataclass
class ApiConstants:
    HOST: str = 'covid-19-statistics.p.rapidapi.com'
    URL: str = 'https://covid-19-statistics.p.rapidapi.com/reports'