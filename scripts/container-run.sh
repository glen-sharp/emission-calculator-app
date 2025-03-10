#!/usr/bin/env bash

cd emission-api
bash emission_calculator_backend/scripts/data-refresh.sh
cd ..

podman build emission-api/. -t emission-api
echo API container image built
podman build emission-frontend/. -t emission-frontend
echo Frontend container image built
podman run -d --name emission-api -p 8000:10 emissions-api:latest
echo API container running. URL: http://127.0.0.1:8000/
podman run -d --name emission-frontend -p 3000:80 emission-frontend:latest
echo Frontend container running. URL: http://localhost:3000/