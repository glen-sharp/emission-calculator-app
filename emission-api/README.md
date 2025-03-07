TODO:
- Allow admin to add or remove data
- Unit tests
- Document data refresh script
- Improve data load script with comments and picking every file in folder
- log error when ingesting data and not passing is_valid() - add try catch as well for date conversion
- Add comments
- Add try catch in shell script
- Don't forget total emissions!!


Assumption:
1. Electricity useage can be rounded to 5 dp
2. In emission factor table, combination of Activity, Lookup identifier and Unit are a unique combination (composite key)
3. Max character length could be up to 200 characters


```bash
bash emission_calculator_backend/scripts/data-refresh.sh
```


Response payload

```json
{
    "air_travel": {
        "total_emissions": <float type>,
        "emissions_array": {
            {
                "co2e": <float type>,
                "scope": <int type>,
                "category": <int type>,
                "activity": <string type>
            }
        }
    },
    "purchased_goods_and_services": {
        "total_emissions": <float type>,
        "emissions_array": {
            {
                "co2e": <float type>,
                "scope": <int type>,
                "category": <int type>,
                "activity": <string type>
            }
        }
    },
    "electricity": {
        "total_emissions": <float type>,
        "emissions_array": {
            {
                "co2e": <float type>,
                "scope": <int type>,
                "category": <int type>,
                "activity": <string type>
            }
        }
    }
}
```