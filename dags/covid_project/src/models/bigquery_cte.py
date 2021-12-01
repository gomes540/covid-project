from dataclasses import dataclass

@dataclass
class BQInfo:
    DATATSET: str = "COVID_RAW"
    TABLE: str = "covid_data"
    
