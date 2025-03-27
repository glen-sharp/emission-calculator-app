import os

EMISSION_FACTOR_INGEST_FOLDER = "./emission_calculator_backend/import/emission_factors/"
AIR_TRAVEL_INGEST_FOLDER = "./emission_calculator_backend/import/air_travel/"
GOODS_AND_SERVICES_INGEST_FOLDER = "./emission_calculator_backend/import/purchased_goods_and_services/"
ELECTRICITY_INGEST_FOLDER = "./emission_calculator_backend/import/electricity/"

MILES_TO_KM_CONVERSION = 1.60934

LOG_LEVEL = "INFO"

ORIGIN = os.environ.get("ORIGIN", "239.255.255.250")
