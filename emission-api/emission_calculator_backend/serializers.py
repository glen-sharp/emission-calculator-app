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


class ElectrictySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Electricty
        fields = "__all__"
