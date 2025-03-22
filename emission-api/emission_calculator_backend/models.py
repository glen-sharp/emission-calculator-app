from django.db import models
import logging
from datetime import datetime
import json

import config


logger = logging.getLogger("root")

#######################
# Helper Functions
#######################


def convert_date(date: str) -> datetime.date:
    """
    Function to convert data string into date type

    :param date: Input date as string type

    :return: Date in as date type
    """
    try:
        date = datetime.strptime(date, "%d/%m/%Y").date()
    except ValueError:
        logger.error(f"Incorrect Air Travel datetime format. Data: {date}")
        raise ValueError(f"Incorrect Air Travel datetime format. Data: {date}")
    return date


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
        verbose_name_plural = "Emission Factors"


class InputEmissionFactors:
    def __init__(self, **kwargs):
        self.activity = kwargs["Activity"].lower()
        self.lookup_identifier = kwargs["Lookup identifiers"].lower()
        self.unit = kwargs["Unit"].lower()
        self.co2e = float(kwargs["CO2e"])
        self.scope = kwargs["Scope"]
        self.category = kwargs["Category"] if kwargs["Category"] else None

    def __str__(self):
        return json.dumps({
            "activity": self.activity,
            "lookup_identifier": self.lookup_identifier,
            "unit": self.unit,
            "co2e": self.co2e,
            "scope": self.scope,
            "category": self.category,
        })


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

    class Meta:
        verbose_name_plural = "Air Travel"


class InputAirTravel:
    def __init__(self, **kwargs):
        self.date = kwargs["Date"]
        self.activity = kwargs["Activity"].lower()
        self.distance_travelled = float(kwargs["Distance travelled"]) if kwargs["Distance travelled"] else 0.0
        self.distance_unit = kwargs["Distance units"].lower()
        self.flight_range = kwargs["Flight range"].lower()
        self.passenger_class = kwargs["Passenger class"].lower()
        self.booking_type = self.flight_range.lower() + ", " + self.passenger_class.lower()
        self.transform_distance_unit()
        self.date = convert_date(self.date)

    def __str__(self):
        return json.dumps({
            "date": str(self.date),
            "activity": self.activity,
            "distance_travelled": self.distance_travelled,
            "distance_unit": self.distance_unit,
            "flight_range": self.flight_range,
            "passenger_class": self.passenger_class,
            "booking_type": self.booking_type,
        })

    def transform_distance_unit(self) -> None:
        """
        Function to validate and transform distance to kilometres
        """
        # Checks if distance unit is miles, if yes, unit is standardised
        if self.distance_unit == "miles":
            # Convert distance to kilometres
            self.distance_travelled = self.distance_travelled * config.MILES_TO_KM_CONVERSION
            self.distance_unit = "kilometres"
        elif self.distance_unit == "kilometres":
            self.distance_travelled = self.distance_travelled
        else:
            logger.error(f"No standard distance unit used. Unit: {self.distance_unit}")
            raise ValueError(f"Air Travel distance unit validation failed. Unit: {self.distance_unit}")


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

    class Meta:
        verbose_name_plural = "Purchased Goods and Services"


class InputPurchasedGoodsAndServices:
    def __init__(self, **kwargs):
        self.date = kwargs["Date"]
        self.activity = kwargs["Activity"].lower()
        self.supplier_category = kwargs["Supplier category"].lower()
        self.spend = float(kwargs["Spend"]) if kwargs["Spend"] else 0.0
        self.spend_unit = kwargs["Spend units"].lower()
        self.date = convert_date(self.date)

    def __str__(self):
        return json.dumps({
            "date": str(self.date),
            "activity": self.activity,
            "supplier_category": self.supplier_category,
            "spend": self.spend,
            "spend_unit": self.spend_unit,
        })


class Electricity(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.CharField(max_length=200, null=False)
    date = models.DateField(null=False)
    country = models.CharField(max_length=200, null=False)
    electricity_usage = models.FloatField(null=False)
    unit = models.CharField(max_length=200, null=False)
    co2e = models.FloatField(null=False)
    scope = models.IntegerField(null=False)
    category = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = "Electricity"


class InputElectricity:
    def __init__(self, **kwargs):
        self.activity = kwargs["Activity"].lower()
        self.date = kwargs["Date"]
        self.country = kwargs["Country"].lower()
        self.electricity_usage = float(kwargs["Electricity Usage"]) if kwargs["Electricity Usage"] else 0.0
        self.unit = kwargs["Units"].lower()
        self.date = convert_date(self.date)

    def __str__(self):
        return json.dumps({
            "activity": self.activity,
            "date": str(self.date),
            "country": self.country,
            "electricity_usage": self.electricity_usage,
            "unit": self.unit,
        })

