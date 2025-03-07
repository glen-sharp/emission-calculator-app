import React from "react";

import { AppBar, Toolbar, Typography } from '@mui/material';


export default function HeaderBar() {
    return (
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" component="div">
                    Emissions Summary
                </Typography>
            </Toolbar>
        </AppBar>
    )
}