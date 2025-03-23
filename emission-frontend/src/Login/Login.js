import React from "react";
import { useState } from "react";

import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';


import './Login.css'
import { UserLogin } from "../utils/serverRequests";

export default function UserLoginInput() {
    // Sets current values for input data
    const [emailValue, setEmailValue] = useState("");
    const [passwordValue, setPasswordValue] = useState("");

    const [errorState, setErrorState] = useState("");

    async function user_login() {
        var contact = {
            email: emailValue,
            password: passwordValue
        };
        try {
            await UserLogin(contact);

            if (errorState) {
                setErrorState("")
            };

            setEmailValue("");
            setPasswordValue("");
        } catch (error) {
            setErrorState(true);
        }
    }

    return (
        <div className="login-input-wrapper">
            <div className="title-wrapper">
                <h1>
                    Emissions Hub Registration
                </h1>
            </div>
            <div>
                <Box
                    component="form"
                    sx={{ '& > :not(style)': { width: '100%' } }}
                    noValidate
                    autoComplete="off"
                >
                    <div className="email-password-wrapper">
                        <div className="text-field">
                            <TextField
                                id="email-input"
                                label="Email"
                                variant="filled"
                                value={emailValue}
                                inputProps={{
                                    maxLength: 100,
                                }}
                                sx={{ width: "15rem" }}
                                onChange={(e) => {
                                    setEmailValue(e.target.value);
                                }}
                                onKeyDown={(e) => {
                                    if (emailValue && passwordValue && e.key === "Enter")
                                        user_login()
                                }}
                            />
                        </div>
                        <div className="text-field">
                            <TextField
                                id="password-input"
                                label="Password"
                                type="password"
                                variant="filled"
                                value={passwordValue}
                                inputProps={{
                                    maxLength: 50,
                                }}
                                sx={{ width: "15rem" }}
                                onChange={(e) => {
                                    setPasswordValue(e.target.value);
                                }}
                                onKeyDown={(e) => {
                                    if (emailValue && passwordValue && e.key === "Enter")
                                        user_login()
                                }}
                            />
                        </div>
                    </div>
                </Box>
            </div>
            <div className="button-error-wrapper">
                    <Button
                        variant="contained"
                        onClick={() => user_login()}
                        disabled={emailValue && passwordValue ? false : true}
                    >Login</Button>
                    {errorState && (
                        <Alert
                            severity="error"
                            style={{ marginTop: '1px', marginLeft: '20px', width: '17em' }}
                        >Oops! Something went wrong.</Alert>
                    )}
            </div>
        </div>
    )
};