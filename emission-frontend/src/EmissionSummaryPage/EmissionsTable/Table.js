import React from "react";

import { DataGrid, gridClasses } from '@mui/x-data-grid';
import Box from '@mui/material/Box';
import { alpha, styled } from '@mui/material/styles';


import './Table.css';

const ODD_OPACITY = 0.2;


export default function EmissionsTable({
    emissions,
}) {

    const columns = [
        { "field": "activity", "headerName": "Activity", width: 300, resizable: false },
        { "field": "scope", "headerName": "Scope", resizable: false },
        { "field": "category", "headerName": "Category", resizable: false },
        { "field": "co2e", "headerName": "CO2e", type: "number", width: 150, resizable: false },
    ];

    function capitalizeWords(string) {
      return string.split(' ').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
      ).join(' ')
    }

    // Add ID field to object to allows DataGrid to visualise
    // and format data attributes
    const emissionsWithIndex = emissions.map((obj, id) => ({
        "id": id,
        "activity": capitalizeWords(obj.activity),
        "scope": obj.scope,
        "category": obj.category ? obj.category : "-",
        "co2e": obj.co2e.toFixed(3),
    }));


    const StripedDataGrid = styled(DataGrid)(({ theme }) => ({
        [`& .${gridClasses.row}.even`]: {
          backgroundColor: theme.palette.grey[200],
          '&:hover': {
            backgroundColor: alpha(theme.palette.primary.main, ODD_OPACITY),
            '@media (hover: none)': {
              backgroundColor: 'transparent',
            },
          },
          '&.Mui-selected': {
            backgroundColor: alpha(
              theme.palette.primary.main,
              ODD_OPACITY + theme.palette.action.selectedOpacity,
            ),
            '&:hover': {
              backgroundColor: alpha(
                theme.palette.primary.main,
                ODD_OPACITY +
                  theme.palette.action.selectedOpacity +
                  theme.palette.action.hoverOpacity,
              ),
              '@media (hover: none)': {
                backgroundColor: alpha(
                  theme.palette.primary.main,
                  ODD_OPACITY + theme.palette.action.selectedOpacity,
                ),
              },
            },
          },
        },
      }));

    return (
        <div className="table-wrapper">
            <Box sx={{
                height: 400,
                width: '47rem'
            }}>
                <StripedDataGrid
                    rows={emissionsWithIndex}
                    columns={columns}
                    disableRowSelectionOnClick
                    hideFooter={true}
                    rowHeight={38}
                    getRowClassName={(params) =>
                        params.indexRelativeToCurrentPage % 2 === 0 ? 'even' : 'odd'
                      }
                />
            </Box>
        </div>
    );
};