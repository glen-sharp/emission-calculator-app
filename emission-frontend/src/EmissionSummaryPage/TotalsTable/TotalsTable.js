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
        {"id": "activity", "name": "Activity"},
        {"id": "total", "name": "Total CO2e"},
    ];

    return (
        <div className="totals-table-wrapper">
            <Paper sx={{width: '30rem'}}>
                <TableContainer component={Paper}>
                    <Table stickyHeader>
                        <TableHead>
                            <TableRow>
                                {columns.map((column)=>(
                                    <TableCell key={column.id}>{column.name}</TableCell>
                                ))}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            <TableRow>
                                <TableCell style={{ width: '40%' }} align="left">Air Travel</TableCell>
                                <TableCell style={{ width: '20%' }}>{totalAirEmissions}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Purchased Goods and Services</TableCell>
                                <TableCell>{totalGoodsAndServicesEmissions}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Electricity</TableCell>
                                <TableCell>{totalElectricityEmissions}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell></TableCell>
                                <TableCell style={{ fontWeight: 600 }}>{totalEmissions}</TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </TableContainer>
            </Paper>
        </div>
    );
}