import csv
from datetime import datetime
import os
import logging

import emission_calculator_backend.serializers as serializers
import emission_calculator_backend.models as models
import config

logger = logging.getLogger("root")


def _data_ingest(ingest_folder_path: str) -> list:
    """
    Reusable component to find CSV file paths in a directory and return the content
    """
    # Find all file paths in ingest folder with .csv extension
    file_paths = [
        file_path for file_path in os.listdir(ingest_folder_path)
        if os.path.splitext(file_path)[1] == ".csv"
    ]

    file_content_array = []

    # Loop through file paths and extract data
    for path in file_paths:
        logger.debug(f"Ingesting: '{path}'")
        with open(f"{ingest_folder_path}{path}", newline="", encoding="utf-8") as file:
            file_content = csv.DictReader(file)
            # Create array with content. In future reuturn only file without creating array (better scalability)
            content = [row for row in file_content]
        file_content_array.append(content)

    return file_content_array


def _emission_factor_data_ingest(emission_factor_path: str) -> None:
    """
    Function to imgest emission factor data via CSV file.
    It ingests all files in the emission factor ingest folder
    """
    for file in _data_ingest(emission_factor_path):
        for emission_factor in file:
            # Create model object using ingested data
            emission_factor_serializer = serializers.EmissionFactorsSerializer(
                data={
                    "activity": emission_factor["Activity"].lower(),
                    "lookup_identifier": emission_factor["Lookup identifiers"].lower(),
                    "unit": emission_factor["Unit"].lower(),
                    "co2e": emission_factor["CO2e"],
                    "scope": emission_factor["Scope"],
                    "category": emission_factor["Category"] if emission_factor["Category"] else None,
                },
            )
            # Execute mandatory input object validator method
            if emission_factor_serializer.is_valid():
                emission_factor_serializer.save()
            else:
                logger.error(f"Ingest data validation failed. Data: {emission_factor}")
                continue
    logger.debug("File ingest complete")
    return


def _air_travel_data_ingest(air_travel_path: str) -> None:
    """
    Function to imgest Air Travel emissions data via CSV file.
    It ingests all files in the Air Travel ingest folder
    """
    for file in _data_ingest(air_travel_path):
        for air_travel in file:
            # Fetch emission factor from mapping table
            emission_factor_obj = models.EmissionFactors.objects.filter(
                activity=air_travel["Activity"].lower(),
                lookup_identifier__contains=air_travel["Passenger class"].lower(),
                unit="kilometres",
            ).filter(
                lookup_identifier__contains=air_travel["Flight range"],
            ).values(
                "co2e",
                "scope",
                "category",
            )

            # Validate only one emission factor entry has been returned for activity
            if len(emission_factor_obj) != 1:
                logger.error(f"Emission factor not found for: {air_travel}")
                continue

            # Checks if distance unit is miles, if yes, unit is standardised
            if air_travel["Distance units"] == "miles":
                # Convert distance to kilometers
                distance_km = float(air_travel["Distance travelled"]) * config.MILES_TO_KM_CONVERSION
            elif air_travel["Distance units"] == "kilometers":
                distance_km = float(air_travel["Distance travelled"])
            else:
                unit = air_travel["Distance units"]
                logger.error(f"No standard distance unit used. Unit: {unit}")
                continue

            try:
                date = datetime.strptime(air_travel["Date"], "%d/%m/%Y").date()
            except ValueError:
                logger.error(f"Incorrect datetime format. Data: {air_travel}")
                continue

            booking_type = air_travel["Flight range"] + ", " + air_travel["Passenger class"]

            # Create model object using ingested data
            air_travel_serializer = serializers.AirTravelSerializer(
                data={
                    "date": date,
                    "activity": air_travel["Activity"].lower(),
                    "distance_travelled": distance_km,
                    "distance_unit": "kilometres",
                    "flight_range": air_travel["Flight range"].lower(),
                    "passenger_class": air_travel["Passenger class"].lower(),
                    "booking_type": booking_type.lower(),
                    # Converting spend to float to allow multiplication with emission factor
                    "co2e": emission_factor_obj[0]["co2e"] * float(distance_km),
                    "scope": emission_factor_obj[0]["scope"],
                    "category": emission_factor_obj[0]["category"],
                },
            )

            # Execute mandatory input object validator method
            if air_travel_serializer.is_valid():
                air_travel_serializer.save()
            else:
                logger.error(f"Ingest data validation failed. Data: {air_travel}, " +
                             f"Reason: {air_travel_serializer.errors}")
                continue
        logger.debug("File ingest complete")


def _good_and_services_data_ingest(goods_services_path: str) -> None:
    """
    Function to imgest Purchased Goods and Services Emission data via CSV file.
    It ingests all files in the Purchased Goods and Services ingest folder
    """
    for file in _data_ingest(goods_services_path):
        for goods_and_services in file:
            # Fetch emission factor from mapping table
            emission_factor_obj = models.EmissionFactors.objects.filter(
                activity=goods_and_services["Activity"].lower(),
                lookup_identifier=goods_and_services["Supplier category"].lower(),
                unit=goods_and_services["Spend units"].lower(),
            ).values(
                "co2e",
                "scope",
                "category",
            )

            # Validate only one emission factor entry has been returned for activity
            if len(emission_factor_obj) != 1:
                logger.error(f"Emission factor not found for: {goods_and_services}")
                continue

            try:
                date = datetime.strptime(goods_and_services["Date"], "%d/%m/%Y").date()
            except ValueError:
                logger.error(f"Incorrect datetime format. Data: {goods_and_services}")
                continue

            # Create model object using ingested data
            goods_and_services_serializer = serializers.PurchasedGoodsAndServicesSerializer(
                data={
                    "date": date,
                    "activity": goods_and_services["Activity"].lower(),
                    "supplier_category": goods_and_services["Supplier category"].lower(),
                    "spend": goods_and_services["Spend"],
                    "spend_unit": goods_and_services["Spend units"].lower(),
                    # Converting spend to float to allow multiplication with emission factor
                    "co2e": emission_factor_obj[0]["co2e"] * float(goods_and_services["Spend"]),
                    "scope": emission_factor_obj[0]["scope"],
                    "category": emission_factor_obj[0]["category"],
                },
            )

            # Execute mandatory input object validator method
            if goods_and_services_serializer.is_valid():
                goods_and_services_serializer.save()
            else:
                logger.error(f"Ingest data validation failed. Data: {goods_and_services}, " +
                             f"Reason: {goods_and_services_serializer.errors}")
                continue


def _electricity_data_ingest(electricity_path: str) -> None:
    """
    Function to imgest Electricity emission data via CSV file.
    It ingests all files in the Electricity ingest folder
    """
    # Find all file paths in ingest folder with .csv extension
    for file in _data_ingest(electricity_path):
        for electricity in file:
            # Fetch emission factor from mapping table
            emission_factor_obj = models.EmissionFactors.objects.filter(
                activity=electricity["Activity"].lower(),
                lookup_identifier=electricity["Country"].lower(),
                unit=electricity["Units"].lower(),
            ).values(
                "co2e",
                "scope",
                "category",
            )

            # Validate only one emission factor entry has been returned for activity
            if len(emission_factor_obj) != 1:
                logger.error(f"Emission factor not found for: {electricity}")
                continue

            try:
                date = datetime.strptime(electricity["Date"], "%d/%m/%Y").date()
            except ValueError:
                logger.error(f"Incorrect datetime format. Data: {electricity}")
                continue

            # Create model object using ingested data
            electricity_serializer = serializers.ElectrictySerializer(
                data={
                    "activity": electricity["Activity"].lower(),
                    "date": date,
                    "country": electricity["Country"].lower(),
                    "electricity_usage": electricity["Electricity Usage"],
                    "unit": electricity["Units"].lower(),
                    # Converting spend to float to allow multiplication with emission factor
                    "co2e": emission_factor_obj[0]["co2e"] * float(electricity["Electricity Usage"]),
                    "scope": emission_factor_obj[0]["scope"],
                    "category": emission_factor_obj[0]["category"],
                },
            )

            # Execute mandatory input object validator method
            if electricity_serializer.is_valid():
                electricity_serializer.save()
            else:
                logger.error(f"Ingest data validation failed. Data: {electricity}, " +
                             f"Reason: {electricity_serializer.errors}")
                continue


def run(
    emission_factor_path: str = config.EMISSION_FACTOR_INGEST_FOLDER,
    air_travel_path: str = config.AIR_TRAVEL_INGEST_FOLDER,
    goods_services_path: str = config.GOODS_AND_SERVICES_INGEST_FOLDER,
    electricity_path: str = config.ELECTRICITY_INGEST_FOLDER,
) -> None:
    """
    Function being run through Django's runscript method

    :param emission_factor_path: Emission Factor data file path
    :param air_travel_path: Air Travel emission data file path
    :param goods_services_path: Purchased Goods & Services emission data file path
    :param electricity_path: Electricity emission data file path
    """
    try:
        # Ingest emission factor data
        _emission_factor_data_ingest(emission_factor_path)
        # Ingest Air Travel emission data
        _air_travel_data_ingest(air_travel_path)
        # Ingest Purchased Goods and Services emission data
        _good_and_services_data_ingest(goods_services_path)
        # Ingest Electricity emission data
        _electricity_data_ingest(electricity_path)
    except Exception as e:
        logger.error(f"Error occurred during data ingestion, see: {e}")
        raise Exception from e
