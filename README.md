# Emission Calculator App

This application consists of a Python Django backend and React Javascript frontend to display Emissions results from ingested data.

Documentation for each of the components can be found here:
- [API Documentation](emission-api/README.md)
- [Frontend Documentation](emission-frontend/README.md)

## Running Locally via Docker

Requirements:
- docker daemon

Before using this method, the required data files need to be in the ingest folders specified [here](emission-api/README.md#data-load), and the user needs to be logged into docker.

Building and starting container images:
```bash
ORIGIN=<host IP address> docker-compose up -d
```

If not value for `ORIGIN` is provided, this will default to `localhost`

Frontend can be accessed via `http://localhost:3000/`

API can be accessed via `http://localhost:8000/`

Stop containers:
```bash
docker-compose stop
```

Remove containers:
```bash
docker-compose rm
```

## Running Locally via Python and Node.js

Requirements:
- python:3.9+
- Node.js v22.4.1+

To run the application locally, the following steps need to be followed.

### API steps as described here: [API local deployment instructions](emission-api/README.md#running-locally)

1. Navigate to API directory 
2. Create and start virtual environment
3. Download required libraries
4. Load data into database
5. Run server locally via Python

### Frontend steps as described here: [Frontend local deployment instructions](emission-frontend/README.md)

1. Navigate to Frontend directory
2. Download Node.js and run required npm terminal commands
