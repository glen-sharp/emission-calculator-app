import React from "react";

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import "./TotalsTable.css"

export default function TotalsTable({
    totalEmissions,
    totalAirEmissions,
    totalGoodsAndServicesEmissions,
    totalElectricityEmissions
}) {
    const columns = [
        {"id": "activity", "name": "Activity", "width": "40%", "align": "left"},
        {"id": "total", "name": "Total CO2e", "width": "40%", "align": "right"},
    ];

    const data = [
        {"id": "air_travel", "activity": "Air Travel", "emission": totalAirEmissions},
        {"id": "good_and_services", "activity": "Purchased Goods and Services", "emission": totalGoodsAndServicesEmissions},
        {"id": "electricity", "activity": "Electricity", "emission": totalElectricityEmissions},
    ]

    return (
        <div className="totals-table-wrapper">
            <Paper sx={{width: '20rem'}}>
                <TableContainer component={Paper}>
                    <Table stickyHeader>
                        <TableHead>
                            <TableRow>
                                {columns.map((val) => (
                                    <TableCell style={{ width: val.width, fontWeight: 600 }} key={val.id} align={val.align}>{val.name}</TableCell>
                                ))}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data.map((val) => (
                                <TableRow key={val.id}>
                                    <TableCell align="left">{val.activity}</TableCell>
                                    <TableCell align="right">{val.emission}</TableCell>
                                </TableRow>
                            ))}
                            <TableRow>
                                <TableCell></TableCell>
                                <TableCell style={{ fontWeight: 600 }} align="right">{totalEmissions}</TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </TableContainer>
            </Paper>
        </div>
    );
}