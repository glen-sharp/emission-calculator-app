import csv
from datetime import datetime
import os

import emission_calculator_backend.serializers as serializers
import emission_calculator_backend.models as models
import config


def emission_factor_data_ingest():
    emission_factor_file_paths = [
        file_path for file_path in os.listdir(config.EMISSION_FACTOR_IMPORT_FOLDER)
        if os.path.splitext(file_path)[1] == ".csv"
    ]
    for path in emission_factor_file_paths:
        with open(f"{config.EMISSION_FACTOR_IMPORT_FOLDER}{path}", newline="", encoding="utf-8") as file:
            emission_factors = csv.DictReader(file)
            for emission_factor in emission_factors:

                emission_factor_serializer = serializers.EmissionFactorsSerializer(
                    data={
                        "activity": emission_factor["Activity"],
                        "lookup_identifier": emission_factor["Lookup identifiers"],
                        "unit": emission_factor["Unit"],
                        "co2e": emission_factor["CO2e"],
                        "scope": emission_factor["Scope"],
                        "category": emission_factor["Category"] if emission_factor["Category"] else None,
                    },
                )
                if emission_factor_serializer.is_valid():
                    emission_factor_serializer.save()
                else:
                    continue


def air_travel_data_ingest():
    air_travel_file_paths = [
        file_path for file_path in os.listdir(config.AIR_TRAVEL_IMPORT_FOLDER)
        if os.path.splitext(file_path)[1] == ".csv"
    ]

    for path in air_travel_file_paths:
        with open(f"{config.AIR_TRAVEL_IMPORT_FOLDER}{path}", newline="", encoding="utf-8") as file:
            air_travel_data = csv.DictReader(file)
            for air_travel in air_travel_data:

                emission_factor_obj = models.EmissionFactors.objects.filter(
                    activity=air_travel["Activity"],
                    lookup_identifier__contains=air_travel["Passenger class"],
                    unit="kilometres",
                ).filter(
                    lookup_identifier__contains=air_travel["Flight range"],
                ).values(
                    "co2e",
                    "scope",
                    "category",
                )[0]

                if air_travel["Distance units"] == "miles":
                    # Convert distance to kilometers
                    distance_km = float(air_travel["Distance travelled"]) * config.MILES_TO_KM_CONVERSION
                elif air_travel["Distance units"] == "kilometers":
                    distance_km = float(air_travel["Distance travelled"])
                else:
                    raise Exception

                air_travel_serializer = serializers.AirTravelSerializer(
                    data={
                        "date": datetime.strptime(air_travel["Date"], "%d/%m/%Y").date(),
                        "activity": air_travel["Activity"],
                        "distance_travelled": distance_km,
                        "distance_unit": "kilometres",
                        "flight_range": air_travel["Flight range"],
                        "passenger_class": air_travel["Passenger class"],
                        # Converting spend to float to allow multiplication with emission factor
                        "co2e": emission_factor_obj["co2e"] * float(distance_km),
                        "scope": emission_factor_obj["scope"],
                        "category": emission_factor_obj["category"],
                    },
                )
                if air_travel_serializer.is_valid():
                    air_travel_serializer.save()
                else:
                    continue


def good_and_services_data_ingest():
    goods_and_services_file_paths = [
        file_path for file_path in os.listdir(config.GOODS_AND_SERVICES_IMPORT_FOLDER)
        if os.path.splitext(file_path)[1] == ".csv"
    ]

    for path in goods_and_services_file_paths:
        with open(f"{config.GOODS_AND_SERVICES_IMPORT_FOLDER}{path}", newline="", encoding="utf-8") as file:
            goods_and_services_data = csv.DictReader(file)
            for goods_and_services in goods_and_services_data:

                # Fetch emission factor from mapping table
                emission_factor_obj = models.EmissionFactors.objects.filter(
                    activity=goods_and_services["Activity"],
                    lookup_identifier=goods_and_services["Supplier category"],
                    unit=goods_and_services["Spend units"],
                ).values(
                    "co2e",
                    "scope",
                    "category",
                )[0]
                goods_and_services_serializer = serializers.PurchasedGoodsAndServicesSerializer(
                    data={
                        "date": datetime.strptime(goods_and_services["Date"], "%d/%m/%Y").date(),
                        "activity": goods_and_services["Activity"],
                        "supplier_category": goods_and_services["Supplier category"],
                        "spend": goods_and_services["Spend"],
                        "spend_unit": goods_and_services["Spend units"],
                        # Converting spend to float to allow multiplication with emission factor
                        "co2e": emission_factor_obj["co2e"] * float(goods_and_services["Spend"]),
                        "scope": emission_factor_obj["scope"],
                        "category": emission_factor_obj["category"],
                    },
                )

                if goods_and_services_serializer.is_valid():
                    goods_and_services_serializer.save()
                else:
                    continue


def electricity_data_ingest():
    electricity_file_paths = [
        file_path for file_path in os.listdir(config.ELECTRICITY_IMPORT_FOLDER)
        if os.path.splitext(file_path)[1] == ".csv"
    ]

    for path in electricity_file_paths:
        with open(f"{config.ELECTRICITY_IMPORT_FOLDER}{path}", newline="", encoding="utf-8") as file:
            electricity_data = csv.DictReader(file)
            for electricity in electricity_data:

                # Fetch emission factor from mapping table
                emission_factor_obj = models.EmissionFactors.objects.filter(
                    activity=electricity["Activity"],
                    lookup_identifier=electricity["Country"],
                    unit=electricity["Units"],
                ).values(
                    "co2e",
                    "scope",
                    "category",
                )[0]
                electricity_serializer = serializers.ElectrictySerializer(
                    data={
                        "activity": electricity["Activity"],
                        "date": datetime.strptime(electricity["Date"], "%d/%m/%Y").date(),
                        "country": electricity["Country"],
                        "electricity_useage": electricity["Electricity Usage"],
                        "unit": electricity["Units"],
                        # Converting spend to float to allow multiplication with emission factor
                        "co2e": emission_factor_obj["co2e"] * float(electricity["Electricity Usage"]),
                        "scope": emission_factor_obj["scope"],
                        "category": emission_factor_obj["category"],
                    },
                )
                if electricity_serializer.is_valid():
                    electricity_serializer.save()
                else:
                    continue


def run():

    emission_factor_data_ingest()

    air_travel_data_ingest()

    good_and_services_data_ingest()

    electricity_data_ingest()
