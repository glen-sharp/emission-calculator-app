from django.test import TestCase, Client
import json
import os
import logging

from emission_calculator_backend.scripts.import_data import run


def test_data_load_helper(test_data_dir: str) -> None:
    """
    Helper function to load test data
    """
    base_path = "./emission_calculator_backend/tests/test_data/"

    run(
        emission_factor_path=os.path.join(base_path, test_data_dir, "emission_factors"),
        air_travel_path=os.path.join(base_path, test_data_dir, "air_travel"),
        goods_services_path=os.path.join(base_path, test_data_dir, "purchased_goods_and_services"),
        electricity_path=os.path.join(base_path, test_data_dir, "electricity"),
    )


class EmissionCalculatorTests(TestCase):

    maxDiff = None

    def setUp(self):
        """
        Set-up method to load test data and start mock API client
        """
        logging.disable(logging.CRITICAL)
        # Execute data load script for test DB using test data paths
        test_data_load_helper("success_test_data")
        self.client = Client()

    def test_api_output(self):
        """
        Test API output.
        Test valid API response schema, and ETL logic for calculating CO2e
        """
        response = self.client.get("/emissions/")

        expected_output = {
            "emissions": {
                "emissions_array": [
                    {
                        "co2e": 3856.8,
                        "scope": 3,
                        "category": 1,
                        "activity": "purchased goods and services",
                    },
                    {
                        "co2e": 1500,
                        "scope": 3,
                        "category": 1,
                        "activity": "purchased goods and services",
                    },
                    {
                        "co2e": 1260,
                        "scope": 3,
                        "category": 1,
                        "activity": "purchased goods and services",
                    },
                    {
                        "co2e": 305.7746,
                        "scope": 3,
                        "category": 6,
                        "activity": "air travel",
                    },
                    {
                        "co2e": 305.7746,
                        "scope": 3,
                        "category": 6,
                        "activity": "air travel",
                    },
                    {
                        "co2e": 153.852904,
                        "scope": 3,
                        "category": 6,
                        "activity": "air travel",
                    },
                    {
                        "co2e": 66,
                        "scope": 2,
                        "category": None,
                        "activity": "electricity",
                    },
                    {
                        "co2e": 38,
                        "scope": 2,
                        "category": None,
                        "activity": "electricity",
                    },
                    {
                        "co2e": 20,
                        "scope": 2,
                        "category": None,
                        "activity": "electricity",
                    },
                    {
                        "co2e": 10,
                        "scope": 2,
                        "category": None,
                        "activity": "electricity",
                    },
                ],
                "total_air_travel_co2e": 765.402104,
                "total_purchased_goods_and_services_co2e": 6616.8,
                "total_electricity_co2e": 134.0,
                "total_co2e": 7516.202104,
            },
        }

        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), expected_output)


class EtlScriptTests(TestCase):

    maxDiff = None

    def setUp(self):
        """
        Set-up method to create test DB and start mock API client
        """
        logging.disable(logging.CRITICAL)
        self.client = Client()

    def test_air_travel_distance(self):
        """
        Testing air travel distances with a combination of miles and kilometres
        """
        test_data_load_helper("air_travel_distance_test_data")

        response = self.client.get("/emissions/")

        expected_output = {
            "emissions": {
                "emissions_array": [
                    {
                        "co2e": 450,
                        "scope": 3,
                        "category": 6,
                        "activity": "air travel",
                    },
                    {
                        "co2e": 305.7746,
                        "scope": 3,
                        "category": 6,
                        "activity": "air travel",
                    },
                    {
                        "co2e": 153.852904,
                        "scope": 3,
                        "category": 6,
                        "activity": "air travel",
                    },
                ],
                "total_air_travel_co2e": 909.6275039999999,
                "total_purchased_goods_and_services_co2e": 0,
                "total_electricity_co2e": 0,
                "total_co2e": 909.6275039999999,
            },
        }

        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), expected_output)

    def test_invalid_date(self):
        """
        Input files include invalid dates that are of format:
        DD-MM-YYYY
        YYYY-MM-DD
        DD/MM/YY

        The correct format is DD/MM/YYYY which is the only type which should be entered into the DB
        """
        test_data_load_helper("invalid_date_test_data")

        response = self.client.get("/emissions/")

        expected_output = {
            "emissions": {
                "emissions_array": [
                    {
                        "co2e": 3856.8,
                        "scope": 3,
                        "category": 1,
                        "activity": "purchased goods and services",
                    },
                    {
                        "co2e": 305.7746,
                        "scope": 3,
                        "category": 6,
                        "activity": "air travel",
                    },
                    {
                        "co2e": 20,
                        "scope": 2,
                        "category": None,
                        "activity": "electricity",
                    },
                ],
                "total_air_travel_co2e": 305.7746,
                "total_purchased_goods_and_services_co2e": 3856.8,
                "total_electricity_co2e": 20,
                "total_co2e": 4182.5746,
            },
        }

        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), expected_output)

    def test_no_file_input(self):
        """
        Testing no input files being places into ingest folders
        """
        test_data_load_helper("no_file_test_data")

        response = self.client.get("/emissions/")

        expected_output = {
            "emissions": {
                "emissions_array": [],
                "total_air_travel_co2e": 0,
                "total_purchased_goods_and_services_co2e": 0,
                "total_electricity_co2e": 0,
                "total_co2e": 0,
            },
        }

        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), expected_output)

    def test_incorrect_emission_factor_column(self):
        """
        Lookup identifiers column of emission factors input file is incorrect.
        Lookup identifiers -> Lookup_Identifiers
        """
        logging.disable(logging.INFO)  # Allowing ERROR logs to run assert method
        with self.assertLogs(logger="root", level="ERROR") as cm:
            test_data_load_helper("incorrect_emission_factors_column_test_data")

            self.assertIn(
                '''ERROR:root:Error occurred during data ingestion, see: "Column validation ''' +
                '''failed for: 'mock_emission_factors.csv' on column: 'Lookup identifiers'"''',
                cm.output,
            )

    def test_incorrect_air_travel_column(self):
        """
        Activity column of air travel input file is incorrect.
        Activity -> Acivity
        """
        logging.disable(logging.INFO)  # Allowing ERROR logs to run assert method
        with self.assertLogs(logger="root", level="ERROR") as cm:
            test_data_load_helper("incorrect_air_travel_column_test_data")

            self.assertIn(
                '''ERROR:root:Error occurred during data ingestion, see: "Column validation ''' +
                '''failed for: 'mock_air_travel.csv' on column: 'Activity'"''',
                cm.output,
            )

    def test_incorrect_electricity_column(self):
        """
        Electricty usage column of electricity input file is incorrect.
        Electricty usage -> Electricty Usage
        """
        logging.disable(logging.INFO)  # Allowing ERROR logs to run assert method
        with self.assertLogs(logger="root", level="ERROR") as cm:
            test_data_load_helper("incorrect_electricity_column_test_data")

            self.assertIn(
                '''ERROR:root:Error occurred during data ingestion, see: "Column validation failed ''' +
                '''for: 'mock_electricity.csv' on column: 'Electricity Usage'"''',
                cm.output,
            )

    def test_incorrect_goods_and_services_column(self):
        """
        Spend units column of purchased goods and services input file is incorrect.
        Spend units -> Spend unit
        """
        logging.disable(logging.INFO)  # Allowing ERROR logs to run assert method
        with self.assertLogs(logger="root", level="ERROR") as cm:
            test_data_load_helper("incorrect_goods_and_services_column_test_data")

            self.assertIn(
                '''ERROR:root:Error occurred during data ingestion, see: "Column validation ''' +
                '''failed for: 'mock_purchased_goods_and_services.csv' on column: 'Spend units'"''',
                cm.output,
            )
