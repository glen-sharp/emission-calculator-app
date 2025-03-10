import React from "react";

import { AppBar, Toolbar, Typography } from '@mui/material';


export default function HeaderBar() {
    return (
        <AppBar position="static" sx={{ bgcolor: "rgba(6, 71, 15, 0.87);" }}>
            <Toolbar>
                <Typography variant="h6" component="div" style={{ fontWeight: 600 }}>
                    Emissions Summary
                </Typography>
            </Toolbar>
        </AppBar>
    )
}