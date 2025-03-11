from django.test import TestCase, Client
import json

from emission_calculator_backend.scripts.import_data import run


class EmissionCalculatorTests(TestCase):
    def setUp(self):
        """
        Set-up method to load test data and start mock API client
        """
        # Execute data load script for test DB using test data paths
        run(
            emission_factor_path="./emission_calculator_backend/tests/test_data/emission_factors/",
            air_travel_path="./emission_calculator_backend/tests/test_data/air_travel/",
            goods_services_path="./emission_calculator_backend/tests/test_data/purchased_goods_and_services/",
            electricity_path="./emission_calculator_backend/tests/test_data/electricity/",
        )
        self.client = Client()
        pass

    def test_api_output(self):
        """
        Test API output.
        Test validates API response schema, and ETL logic for calculating CO2e
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
                        "co2e": 1500.0,
                        "scope": 3,
                        "category": 1,
                        "activity": "purchased goods and services",
                    },
                    {
                        "co2e": 1260.0,
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
                        "co2e": 66.0,
                        "scope": 2,
                        "category": None,
                        "activity": "electricity",
                    },
                    {
                        "co2e": 38.0,
                        "scope": 2,
                        "category": None,
                        "activity": "electricity",
                    },
                    {
                        "co2e": 20.0,
                        "scope": 2,
                        "category": None,
                        "activity": "electricity",
                    },
                    {
                        "co2e": 10.0,
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
