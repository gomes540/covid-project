# Covid-19 ELT Project

This project consists in create a Data Lake and a Data Warehouse extracting daily data from an Covid-19 API. It involves tecnologies that are commonly used in Data Enginnering.
This repository contains only that Extract and Load part of the ELT, you can look the Transformation part in https://github.com/gomes540/dbt-projects.

## Usage

1. - Set up the Airflow

NOTE: I recommend you to access the Airflow Documentation to set up the airflow:

`https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html`

 - Create a `.env`

     run: `echo -e "AIRFLOW_UID=$(id -u)" > .env`. If you are not using Linux the value should be: `AIRFLOW_UID=50000`
     
 - run `docker-compose up airflow-init`
 
 - run `docker-compose up -d`
  
 - Acess your `http://localhost:8080/`

 - You can see the username and the password in the fields `_AIRFLOW_WWW_USER_USERNAME` and `_AIRFLOW_WWW_USER_PASSWORD` in the `docker-compose.yml` file

     1.1 - Variables in airflow
     
      - `covid_api_key`: your api key

      - `project_id`: your project id

      - `covid_project_service_account_secret`: your GCP Service Account


2. Get API Key

 - Access `https://rapidapi.com/axisbits-axisbits-default/api/covid-19-statistics/` and get your API Key

     Note: This Key is the `covid_api_key` variable in Airflow


3. Google Cloud Platform (GCP)

 - Create one Service Account for the project

     Go to `IAM & Admin` -> `Service Accounts`
     
     Then, create the Service Account with the roles `BigQuery Admin` and `Storage Admin`, then create a json key and download it. 
     
     Note: This credential is the `covid_project_service_account_secret` variable in Airflow

 - Create a Bucket in Cloud Storage
 
      Create a Bucket called `api-covid`.
      
      ![image](https://user-images.githubusercontent.com/72705868/146656604-833be9aa-d9ea-4e51-af8c-12925877b9c9.png)
      
      The project will use this Bucket to save the data extracted from the API.

 - Create a Dataset in BigQuery

     Create a Dataset called `COVID_DATA_RAW`
     
     ![image](https://user-images.githubusercontent.com/72705868/146656562-6a7a9562-a480-4fed-b69f-188bb242b470.png)
     
     The project will use this Dataset to create a table called `covid-data` which contains the raw API Covid data.
     
Now you can run the dag `elt_covid_project`!

 

