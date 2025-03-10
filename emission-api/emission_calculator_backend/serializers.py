from rest_framework import serializers
import emission_calculator_backend.models as models


class EmissionFactorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmissionFactors
        fields = "__all__"


class AirTravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AirTravel
        fields = "__all__"


class PurchasedGoodsAndServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchasedGoodsAndServices
        fields = "__all__"


class ElectricitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Electricity
        fields = "__all__"
