from enum import Enum

class ApiConstants(Enum):
    HOST: str = 'covid-19-statistics.p.rapidapi.com'
    URL: str = 'https://covid-19-statistics.p.rapidapi.com/reports'

class RequestMethod(Enum):
    GET: str = "GET"