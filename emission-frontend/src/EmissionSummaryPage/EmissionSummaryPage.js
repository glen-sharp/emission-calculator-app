import React from "react";
import { useState, useEffect } from "react";

import { GetEmissions } from "../utils/serverRequests";
import TotalsTable from "./TotalsTable/TotalsTable";
import EmissionsTable from "./EmissionsTable/Table";
import "./EmissionSummaryPage.css";

export default function EmissionsPage() {

    const [emissions, setEmissions] = useState([])
    const [totalEmissions, setTotalEmissions] = useState("")

    const [totalAirEmissions, setTotalAirEmissions] = useState("")

    const [totalGoodsAndServicesEmissions, setTotalGoodsAndServicesEmissions] = useState("")

    const [totalElectricityEmissions, setTotalElectricityEmissions] = useState("")

    async function getData() {
        const response = await GetEmissions()
        const data = await response.json()

        setEmissions(data.emissions.emissions_array)

        setTotalEmissions(data.emissions.total_co2e.toFixed(3))

        setTotalAirEmissions(data.emissions.total_air_travel_co2e.toFixed(3))
        setTotalGoodsAndServicesEmissions(data.emissions.total_purchased_goods_and_services_co2e.toFixed(3))
        setTotalElectricityEmissions(data.emissions.total_electricity_co2e.toFixed(3))
    }
    useEffect(() => {
        getData()
    }, [])

    return (
        <div className="emissions-page-wrapper">
            <EmissionsTable
                emissions={emissions}
            />
            <TotalsTable
                totalEmissions={totalEmissions}
                totalAirEmissions={totalAirEmissions}
                totalGoodsAndServicesEmissions={totalGoodsAndServicesEmissions}
                totalElectricityEmissions={totalElectricityEmissions}
            />
        </div>
    );
};