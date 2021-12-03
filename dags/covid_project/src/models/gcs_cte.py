from enum import Enum

class FilePath(Enum):
    BUCKET: str = "api-covid"
    FILENAME: str = "covid-data.csv"
    
class FileType(Enum):
    CONTENT_TYPE: str = "text/csv"
    
    