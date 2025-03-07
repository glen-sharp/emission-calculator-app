from rest_framework.decorators import api_view
from rest_framework.response import Response

import emission_calculator_backend.models as models


@api_view(["GET"])
def emissions(request):
    """
    Function returning emission data for each activity
    """

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
    output = list(air_travel.union(purchased_goods_and_services, electricity, all=True))

    # Calculate total CO2e values for each activity
    air_travel_total = sum(obj["co2e"] for obj in list(air_travel))
    purchased_goods_and_services_total = sum(obj["co2e"] for obj in list(purchased_goods_and_services))
    electricity_total = sum(obj["co2e"] for obj in list(electricity))

    # Calculate total CO2e across all activities
    total = air_travel_total + purchased_goods_and_services_total + electricity_total

    response = {
        "emissions": {
            "emissions_array": output,
            "total_air_travel_co2e": air_travel_total,
            "total_purchased_goods_and_services_co2e": purchased_goods_and_services_total,
            "total_electricity_co2e": electricity_total,
            "total_co2e": total,
        },
    }

    return Response(response)
