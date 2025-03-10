#!/usr/bin/env bash

set -e

if [ $# -eq 0 ]; then
  echo "Error: No parameter provided"
  exit 1
fi

# Using parameter to allow use of different image build software
CONTAINER_APP=$1

cd emission-api
bash emission_calculator_backend/scripts/data-refresh.sh
cd ..

$CONTAINER_APP build emission-api/. -t emission-api
echo API container image built
$CONTAINER_APP build emission-frontend/. -t emission-frontend
echo Frontend container image built
$CONTAINER_APP run -d --name emission-api -p 8000:10 emission-api:latest
echo API container running. URL: http://localhost:8000/
$CONTAINER_APP run -d --name emission-frontend -p 3000:80 emission-frontend:latest
echo Frontend container running. URL: http://localhost:3000/