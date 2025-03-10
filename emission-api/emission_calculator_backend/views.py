from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
import logging

import emission_calculator_backend.models as models

logger = logging.getLogger("root")


@api_view(["GET"])
def emissions(request) -> Response:
    """
    Function returning emission data for each activity
    """
    try:
        # Query for all air travel emission info
        air_travel = models.AirTravel.objects.values(
            "co2e",
            "scope",
            "category",
            "activity",
        )

        # Query for all purchased goods and services emission info
        purchased_goods_and_services = models.PurchasedGoodsAndServices.objects.values(
            "co2e",
            "scope",
            "category",
            "activity",
        )

        # Query for all electricity emission info
        electricity = models.Electricty.objects.values(
            "co2e",
            "scope",
            "category",
            "activity",
        )

        # Union all tables together
        output = air_travel.union(purchased_goods_and_services, electricity, all=True).order_by("-co2e")

        # Calculate total CO2e values for each activity
        air_travel_total = models.AirTravel.objects.aggregate(Sum("co2e"))["co2e__sum"]
        purchased_goods_and_services_total = models.PurchasedGoodsAndServices.objects.aggregate(
            Sum("co2e"),
        )["co2e__sum"]
        electricity_total = models.Electricty.objects.aggregate(Sum("co2e"))["co2e__sum"]

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
