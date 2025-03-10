# Emissions Calculator Backend

This backend repository contains an ETL script that uses CSV files from ingest folders, and populates tables in a SQLite database with Emissions data. Integrated with the database is a REST API that uses the Python Django web framework to query the data.

The API currently handles Emissions data for:
- Air Travel
- Purchased Goods and Services
- Electricity

## ETL Script

To execute the ETL stage, the following query is run:
```bash
bash emission_calculator_backend/scripts/data-refresh.sh
```

Steps: 
1. Deletes the current SQLite database
2. Creates a new DB using the DB schema in the `models.py` file
3. (Through execution of ETL script) Finds all CSV files in the ingest folders
4. Extracts data from CSV files
5. Data validation (if failed, current entry is logged and skipped)
6. Performs simple data transformations (eg. lowering case of text, converting units)
7. Loads relevant tables with data

## GET /emissions

Response payload:

```json
{
    "emissions": {
        "emissions_array": [
            {
                "co2e": <float type>,
                "scope": <int type>,
                "category": <int type>,
                "activity": <string type>
            }
        ],
        "total_air_travel_co2e": <float type>,
        "total_purchased_goods_and_services_co2e": <float type>,
        "total_electricity_co2e": <float type>,
        "total_co2e": <float type>
    }
}
```

## Formatting

Throughout development of this code, the PEP8 style guide was followed.
The following style decisions were used:
1. Max line length: 100
2. Quote type: double

Static code analysis can be run through:
```bash
flake8
```

## Configurable Variables

In the `config.py` file, there are various configurable parameters. These include:

| Variable Name                      | Data Type | Description                                                                  | 
| ---------------------------------- | --------- | ---------------------------------------------------------------------------- |
| EMISSION_FACTOR_INGEST_FOLDER      | dict      | Folder path containing Emission Factor data files                            |
| AIR_TRAVEL_INGEST_FOLDER           | float     | Folder path containing Air Travel Emissions data files                       |
| GOODS_AND_SERVICES_INGEST_FOLDER   | int       | Folder path containing Purchased Goods and Services Emissions data files     |
| ELECTRICITY_INGEST_FOLDER          | int       | Folder path containing Electricity Emissions dats files                      |
| MILES_TO_KM_CONVERSION             | int       | Corefficient to convert Miles -> Kilometers                                  |
| LOG_LEVEL                          | str       | Level for types of logs output to stdout                                     |


## Assumptions

1. Electricity useage can be rounded to 5 dp
2. In emission factor table, combination of Activity, Lookup identifier and Unit are a unique combination (composite key)
3. Max character length could be up to 200 characters
4. 'lookup_identifier' is not unique in EmissionFactors table
5. Null category for electricity emission factors should not be transformed
6. Air Travel lookup value will always be in format: "<flight range>, <passenger class>"
7. Whenever new emission factor datadata or activity data is available, the ETL pipeline can be run to refresh DB
8. Data is not manually changed in the DB or via admin role

## Executing locally

### Creating and Starting a Virtual Environment

Best way to download the required python packages and run the app locally is to start a virtual environment

```bash
pip install virtualenv
python -m venv <virtual-environment-name>
source <virtual-environment-name>/bin/activate
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

To run the server via a Docker image, execute the following commands:
```bash
docker build . -t emission-api

docker run -p 8000:10 emission-api:latest
```

### Unit Test Execution
Execute following in terminal:
```bash
python manage.py test emission_calculator_backend/tests --verbosity=2
```

## Future Improvements
1. Add foregn key constraint between tables and query the Scope and Category through that
    - Means that most up-to-date Scope and Category is used
    - Couldn't get done now as don't know if 'lookup_identifier' is unique so can't just filter on that without using unit field
    - Also results in extra table to be queried, potentially resulting API being less performant
2. Split database into "raw" and "conform" instances to allow raw data to be queries alongside transformed data
3. Use environment variables for variables in `config.py` file

