# Emissions Calculator Backend

This backend repository contains an ETL script that uses CSV files from ingest folders, and populates tables in a SQLite database with Emissions data. Integrated with the database is a REST API that uses the Python Django web framework to query the data.

The API currently handles Emissions data for:
- Air Travel
- Purchased Goods and Services
- Electricity

## Contents
- [ETL Script](#etl-script)
- [Running locally](#running-locally)
    - [Creating and Starting a Virtual Environment](#creating-and-starting-a-virtual-environment)
    - [Downloading Required Libraries](#downloading-required-libraries)
    - [Data Load](#data-load)
    - [Running Server Locally](#running-server-locally)
    - [Unit Test Execution](#unit-test-execution)
    - [Formatting](#formatting)
- [GET /emissions/](#get-emissions)
- [Configurable Variables](#configurable-variables)
- [Assumptions](#assumptions)
- [Future Improvements](#future-improvements)

## ETL Script

To execute the ETL stage, the following query is run in the `emission-api` directory:
```bash
bash emission_calculator_backend/scripts/data-refresh.sh
```

Steps:
1. Executes unit tests
2. Deletes the current SQLite database
3. Creates a new DB using the DB schema in the `models.py` file
4. (Through execution of ETL script) Finds all CSV files in the ingest folders
5. Extracts data from CSV files
6. Through 'Input' layer objects, apply data validation (if failed, current entry is logged and skipped)
7. Performs simple data transformations:
    - All strings are converted to lower-case
    - Air travel distance unit is converted to kilometres
8. Loads relevant tables with data

## Running locally

### Creating and Starting a Virtual Environment

Best way to download the required python packages and run the app locally is to start a virtual environment

```bash
pip3 install virtualenv
python3 -m venv .venv
source .venv/bin/activate
```

### Downloading Required Libraries

These libraries should not be treated as production code dependencies, hence the 'dev' prefix

```bash
pip install -r requirements.txt
```

### Data Load

Before running server locally, data must be loaded into the DB in CSV format.

It is recommended that all input files are placed in the following directory:

```bash
emission-api/
|
|-- emission_calculator_backend/
    |-- import/
        |-- air_travel/
        |-- electricity/
        |-- emission_factors/
        |-- purchased_goods_and_services/
```

Execution of the following command will run the ETL script.

```bash
bash emission_calculator_backend/scripts/data-refresh.sh
```

### Running Server Locally

To run the server locally using python, execute:
```bash
python manage.py runserver
```

To run the server via a Docker image, execute the following commands after adding the relevant files to the ingest folders:
```bash
docker build . -t emission-api

docker run -p 8000:10 emission-api:latest
```

The server is now available using the following URL: `http://localhost:3000/`

The API can be queried in the terminal with the following cURL command:

```bash
curl --location 'http://127.0.0.1:8000/emissions'
```

### Unit Test Execution
Execute following in terminal:
```bash
python manage.py test emission_calculator_backend/tests --verbosity=2
```

### Formatting

Throughout development of this code, the PEP8 style guide was followed.
The following style decisions were used:
1. Max line length: 120
2. Quote type: double

Static code analysis can be run through:
```bash
flake8
```

## GET /emissions/

Response payload:

```json
{
    "emissions": {
        "emissions_array": [
            {
                "co2e": "<float type>",
                "scope": "<int type>",
                "category": "<int type>",
                "activity": "<string type>"
            }
        ],
        "total_air_travel_co2e": "<float type>",
        "total_purchased_goods_and_services_co2e": "<float type>",
        "total_electricity_co2e": "<float type>",
        "total_co2e": "<float type>"
    }
}
```


## Configurable Variables

In the `config.py` file, there are various configurable parameters. These include:

| Variable Name                      | Data Type | Description                                                                  | 
| ---------------------------------- | --------- | ---------------------------------------------------------------------------- |
| EMISSION_FACTOR_INGEST_FOLDER      | str       | Folder path containing Emission Factor data files                            |
| AIR_TRAVEL_INGEST_FOLDER           | str       | Folder path containing Air Travel Emissions data files                       |
| GOODS_AND_SERVICES_INGEST_FOLDER   | str       | Folder path containing Purchased Goods and Services Emissions data files     |
| ELECTRICITY_INGEST_FOLDER          | str       | Folder path containing Electricity Emissions dats files                      |
| MILES_TO_KM_CONVERSION             | float     | Coefficient to convert Miles -> Kilometres                                  |
| LOG_LEVEL                          | str       | Level for types of logs output to stdout                                     |


## Unit Tests

| Test No. | Test Case Group           | Test Func Name                                   | Description                                                                  |
| -------- | ------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------- |
| 1.       | Emission Calculator Tests | ```test_api_output()```                          | Test valid API response schema, and ETL logic for calculating CO2e           |
| 2.       | ETL Script Test           | ```test_air_travel_distance()```                 | Testing air travel distances with a combination of miles and kilometres      |
| 3.       | ETL Script Test           | ```test_invalid_date()```                        | Test files with invalid date format                                          |
| 4.       | ETL Script Test           | ```test_no_file_input()```                       | Testing empty ingest folders                                                 |
| 5.       | ETL Script Test           | ```test_incorrect_emission_factor_column()```    | Lookup identifiers column of emission factors input file is incorrect        |
| 6.       | ETL Script Test           | ```test_incorrect_air_travel_column()```         | Activity column of air travel input file is incorrect                        |
| 7.       | ETL Script Test           | ```test_incorrect_electricity_column()```        | Electricty usage column of electricity input file is incorrect               |
| 8.       | ETL Script Test           | ```test_incorrect_goods_and_services_column()``` | Spend units column of purchased goods and services input file is incorrect   |



## Assumptions

1. In emission factors table, the combination of Activity, Lookup identifier and Unit are unique (composite key)
2. Max character length could be up to 200 characters
3. `lookup_identifier` is not unique in EmissionFactors table
4. Null category for electricity emission factors should not be transformed
5. Air Travel lookup value will always be in format: `<flight range>, <passenger class>`
6. Whenever new emission factor data or activity data is available, the ETL pipeline can be run to refresh DB
7. Data is not manually changed in the DB or via admin role
8. Emission Factors data is static and will not change
9. Activity groups can be hard-coded, and therefore if new activities are ingested, this will be added to the API


## Future Improvements
1. Potentially add foregn key constraint between fact and dimension tables, and query the Scope and Category through that if `lookup_identifier` is unique
    - Means that most up-to-date Scope and Category is used
    - Results in extra table to be queried, potentially making API being less performant
2. Split database into "raw" and "conform" instances to allow raw data to be queries alongside transformed data
3. Data type validation for input CSV files
4. Use environment variables for variables in `config.py` file
5. Run ETL pipeline for non-emission factor files asynchronously using eg Celery
5. Create CI/CD pipeline that runs unit tests, static code analysis and pushes container images to a container registry then deploys
5. Deploying to AWS:
    1. Replace import folder with S3 bucket
    2. Allow Athena to query raw CSV files
    3. Convert ETL script into Glue job
    4. Link eventbridge with S3 bucket, and trigger glue job when file is loaded
    5. Populate RDS with conformed data from glue job
    6. Push API and Frontend container image to ECR
    7. Deploy API into AWS Lambda using API gateway to query
    8. Deploy Frontend into AWS Fargate
