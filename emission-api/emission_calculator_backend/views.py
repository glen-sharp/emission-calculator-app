from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Model
import logging

import emission_calculator_backend.models as models

logger = logging.getLogger("root")

#######################
# Helper Functions
#######################


def fetch_activity_query(activity_model: Model):
    """
    Function returning query containing activity fields

    :param activity_model: Django model for activity

    :return: Activity data query
    """
    query = activity_model.objects.values(
        "co2e",
        "scope",
        "category",
        "activity",
    )

    return query


def fetch_emission_total(activity_model: Model):
    """
    Function returning total for CO2e for a specific activity

    :param activity_model: Django model for activity

    :return: CO2e total
    """
    db_total = activity_model.objects.aggregate(Sum("co2e"))["co2e__sum"]

    total = db_total if db_total else 0

    return total

#######################
# API Views
#######################


@api_view(["GET"])
def emissions(request) -> Response:
    """
    Function returning emission data for each activity
    """
    try:
        # Query for all air travel emission info
        air_travel = fetch_activity_query(models.AirTravel)

        # Query for all purchased goods and services emission info
        purchased_goods_and_services = fetch_activity_query(models.PurchasedGoodsAndServices)

        # Query for all electricity emission info
        electricity = fetch_activity_query(models.Electricity)

        # Union all tables together
        output = air_travel.union(purchased_goods_and_services, electricity, all=True).order_by("-co2e")

        # Calculate total CO2e values for each activity. If None is returned, default to 0
        air_travel_total = fetch_emission_total(models.AirTravel)
        purchased_goods_and_services_total = fetch_emission_total(models.PurchasedGoodsAndServices)
        electricity_total = fetch_emission_total(models.Electricity)

        # Calculate total CO2e across all activities
        total = air_travel_total + purchased_goods_and_services_total + electricity_total

        response = {
            "emissions": {
                "emissions_array": list(output),
                "total_air_travel_co2e": air_travel_total,
                "total_purchased_goods_and_services_co2e": purchased_goods_and_services_total,
                "total_electricity_co2e": electricity_total,
                "total_co2e": total,
            },
        }

        return Response(response)
    except Exception as e:
        logger.error(f"Internal server error occurred, see: {e}")
        return Response({"message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
