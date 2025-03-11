import csv
import os
import logging

import emission_calculator_backend.serializers as serializers
import emission_calculator_backend.models as models
import config

logger = logging.getLogger("root")


def _data_ingest(ingest_folder_path: str, input_class) -> list:
    """
    Reusable component to find CSV file paths in a directory and return the content

    :param ingest_folder_path: Folder path containing files to be ingested

    :return: Array with objects containing CSV data
    """
    # Find all file paths in ingest folder with .csv extension
    try:
        file_paths = [
            file_path for file_path in os.listdir(ingest_folder_path)
            if os.path.splitext(file_path)[1] == ".csv"
        ]
    except FileNotFoundError as e:
        logger.error(f"No directory found. See {e}")
        return []

    file_content_array = []
    content = []

    # Loop through file paths and extract data
    for path in file_paths:
        logger.info(f"Ingesting: '{path}'")
        with open(os.path.join(ingest_folder_path, path), newline="", encoding="utf-8") as file:
            file_content = csv.DictReader(file)
            try:
                # Create array of objects with content. In future return only
                # file without creating array (better scalability)
                for row in file_content:
                    try:
                        content.append(input_class(**row))
                    except ValueError:
                        # If value error returned, this means data validation has failed,
                        # and this row will be skipped
                        continue
            except KeyError as e:
                raise KeyError(f"Column validation failed for: '{path}' on column: {e}")
        file_content_array.append(content)

    return file_content_array


def _fetch_emission_factor_object(
    activity: str,
    lookup_identifier: str,
    unit: str,
) -> models.EmissionFactors:
    """
    Function to return emission factor object

    :param activity: Activity name
    :param lookup_identifier: Identifier for specific activity
    :param unit: Unit of measure for activity

    :return: Emission Factor object
    """
    emission_factor_obj = models.EmissionFactors.objects.filter(
        activity=activity,
        lookup_identifier=lookup_identifier,
        unit=unit,
    ).first()  # first() method can be used due to unique_together property in model

    return emission_factor_obj


def _emission_factor_data_ingest(emission_factor_path: str) -> None:
    """
    Function to ingest emission factor data via CSV file.
    It ingests all files in the emission factor ingest folder

    :param emission_factor_path: File path containing emission factor files
    """
    for file in _data_ingest(emission_factor_path, models.InputEmissionFactors):
        for emission_factor_obj in file:
            # Create model object using ingested data
            emission_factor_serializer = serializers.EmissionFactorsSerializer(
                data={
                    "activity": emission_factor_obj.activity,
                    "lookup_identifier": emission_factor_obj.lookup_identifier,
                    "unit": emission_factor_obj.unit,
                    "co2e": emission_factor_obj.co2e,
                    "scope": emission_factor_obj.scope,
                    "category": emission_factor_obj.category,
                },
            )
            # Execute mandatory input object validator method
            if emission_factor_serializer.is_valid():
                emission_factor_serializer.save()
            else:
                logger.error(f"Ingest data validation failed. Data: {emission_factor_obj}")
                continue
    logger.info("Emission factor files ingest complete")


def _air_travel_data_ingest(air_travel_path: str) -> None:
    """
    Function to ingest Air Travel emissions data via CSV file.
    It ingests all files in the Air Travel ingest folder

    :param air_travel_path: File path containing air travel emission files
    """
    for file in _data_ingest(air_travel_path, models.InputAirTravel):
        for air_travel_obj in file:
            # Fetch emission factor from mapping table
            emission_factor_obj = _fetch_emission_factor_object(
                activity=air_travel_obj.activity,
                lookup_identifier=air_travel_obj.booking_type,
                unit="kilometres",
            )

            # Validate one emission factor entry has been returned for activity
            if not emission_factor_obj:
                logger.error(f"Emission factor not found for: {air_travel_obj}")
                continue

            # Create model object using ingested data
            air_travel_serializer = serializers.AirTravelSerializer(
                data={
                    "date": air_travel_obj.date,
                    "activity": air_travel_obj.activity,
                    "distance_travelled": air_travel_obj.distance_travelled,
                    "distance_unit": "kilometres",
                    "flight_range": air_travel_obj.flight_range,
                    "passenger_class": air_travel_obj.passenger_class,
                    "booking_type": air_travel_obj.booking_type,
                    # Converting spend to float to allow multiplication with emission factor
                    "co2e": emission_factor_obj.co2e * air_travel_obj.distance_travelled,
                    "scope": emission_factor_obj.scope,
                    "category": emission_factor_obj.category,
                },
            )

            # Execute mandatory input object validator method
            if air_travel_serializer.is_valid():
                air_travel_serializer.save()
            else:
                logger.error(f"Ingest data validation failed. Data: {air_travel_obj}, " +
                             f"Reason: {air_travel_serializer.errors}")
                continue
    logger.info("Air travel files ingest complete")


def _good_and_services_data_ingest(goods_services_path: str) -> None:
    """
    Function to ingest Purchased Goods and Services Emission data via CSV file.
    It ingests all files in the Purchased Goods and Services ingest folder

    :param goods_services_path: File path containing purchased goods and services emission files
    """
    for file in _data_ingest(goods_services_path, models.InputPurchasedGoodsAndServices):
        for goods_and_services in file:
            # Fetch emission factor from mapping table
            emission_factor_obj = _fetch_emission_factor_object(
                activity=goods_and_services.activity,
                lookup_identifier=goods_and_services.supplier_category,
                unit=goods_and_services.spend_unit,
            )

            # Validate only one emission factor entry has been returned for activity
            if not emission_factor_obj:
                logger.error(f"Emission factor not found for: {goods_and_services}")
                continue

            # Create model object using ingested data
            goods_and_services_serializer = serializers.PurchasedGoodsAndServicesSerializer(
                data={
                    "date": goods_and_services.date,
                    "activity": goods_and_services.activity,
                    "supplier_category": goods_and_services.supplier_category,
                    "spend": goods_and_services.spend,
                    "spend_unit": goods_and_services.spend_unit,
                    # Converting spend to float to allow multiplication with emission factor
                    "co2e": emission_factor_obj.co2e * goods_and_services.spend,
                    "scope": emission_factor_obj.scope,
                    "category": emission_factor_obj.category,
                },
            )

            # Execute mandatory input object validator method
            if goods_and_services_serializer.is_valid():
                goods_and_services_serializer.save()
            else:
                logger.error(f"Ingest data validation failed. Data: {goods_and_services}, " +
                             f"Reason: {goods_and_services_serializer.errors}")
                continue
    logger.info("Purchased goods and services files ingest complete")


def _electricity_data_ingest(electricity_path: str) -> None:
    """
    Function to ingest Electricity emission data via CSV file.
    It ingests all files in the Electricity ingest folder

    :param electricity_path: File path containing electricity emission files
    """
    # Find all file paths in ingest folder with .csv extension
    for file in _data_ingest(electricity_path, models.InputElectricity):
        for electricity in file:
            # Fetch emission factor from mapping table
            emission_factor_obj = _fetch_emission_factor_object(
                activity=electricity.activity,
                lookup_identifier=electricity.country,
                unit=electricity.unit,
            )

            # Validate an emission factor entry has been returned for activity
            if not emission_factor_obj:
                logger.error(f"Emission factor not found for: {electricity}")
                continue

            # Create model object using ingested data
            electricity_serializer = serializers.ElectricitySerializer(
                data={
                    "activity": electricity.activity,
                    "date": electricity.date,
                    "country": electricity.country,
                    "electricity_usage": electricity.electricity_usage,
                    "unit": electricity.unit,
                    # Converting spend to float to allow multiplication with emission factor
                    "co2e": emission_factor_obj.co2e * float(electricity.electricity_usage),
                    "scope": emission_factor_obj.scope,
                    "category": emission_factor_obj.category,
                },
            )

            # Execute mandatory input object validator method
            if electricity_serializer.is_valid():
                electricity_serializer.save()
            else:
                logger.error(f"Ingest data validation failed. Data: {electricity}, " +
                             f"Reason: {electricity_serializer.errors}")
                continue
    logger.info("Electricity files ingest complete")


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
