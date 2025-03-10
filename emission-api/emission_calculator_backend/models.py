from django.db import models


class EmissionFactors(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.CharField(max_length=200, null=False)
    lookup_identifier = models.CharField(max_length=200, null=False)
    unit = models.CharField(max_length=200, null=False)
    co2e = models.FloatField(null=False)
    scope = models.IntegerField(null=False)
    category = models.IntegerField(null=True)

    class Meta:
        unique_together = (("activity", "lookup_identifier", "unit"))


class AirTravel(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=False)
    activity = models.CharField(max_length=200, null=False)
    distance_travelled = models.FloatField(null=False)
    distance_unit = models.CharField(max_length=200, null=False)
    flight_range = models.CharField(max_length=200, null=False)
    passenger_class = models.CharField(max_length=200, null=False)
    booking_type = models.CharField(max_length=200, null=False)
    co2e = models.FloatField(null=False)
    scope = models.IntegerField(null=False)
    category = models.IntegerField(null=True)


class PurchasedGoodsAndServices(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=False)
    activity = models.CharField(max_length=200, null=False)
    supplier_category = models.CharField(max_length=200, null=False)
    spend = models.BigIntegerField(null=False)
    spend_unit = models.CharField(max_length=200, null=False)
    co2e = models.FloatField(null=False)
    scope = models.IntegerField(null=False)
    category = models.IntegerField(null=True)


class Electricty(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.CharField(max_length=200, null=False)
    date = models.DateField(null=False)
    country = models.CharField(max_length=200, null=False)
    electricity_usage = models.FloatField(null=False)
    unit = models.CharField(max_length=200, null=False)
    co2e = models.FloatField(null=False)
    scope = models.IntegerField(null=False)
    category = models.IntegerField(null=True)
