docs = """
## COVID PROJECT DAG

### Goal 
Extract daily data from COVID API, save this data in a Data Lake in csv format and then upload this csv data into a paritioned 
raw table by day in the Data Warehouse.
This DAG is part of the ELT Process, more specifically the Extract and Load part. For the Transformation part we're using the
DBT. For this project we're using the GCP Stack.

This dag runs every day at 4:30 AM UTC.

API: https://rapidapi.com/axisbits-axisbits-default/api/covid-19-statistics/

### DAG Configuration

1. Follow the README instructions for the project and configure these environment variables:

    `api_key` - Your api key.
    
    `project_id` - The Project ID of your project in Google Cloud Platform (GCP).
    
    `covid_project_service_account` - The Service Account that you need to create in your GCP project.
    
### Trigger Example:

1. Optional

    - `"start_date":"YYYY-DD-MM"`
    
    - `"end_date":"YYYY-DD-MM"`
    
    
    If `start_date` and `end_date` are passed set, the DAG is going to extract data from API from `start_date` to `end_date`

    
    Example:
    ```
    {
        "start_date":"2021-12-01", "end_date":"2021-12-10"
    }
    ```

    Note: If `start_date` and `end_date` are not passed, the dag will extract data from the previous day of the trigger day.

"""
