#!/usr/bin/env bash

set -e

docker build emission-api/. -t emission-api
echo API container image built
docker build emission-frontend/. -t emission-frontend
echo Frontend container image built
docker run -d --name emission-api -p 8000:10 emission-api:latest
echo API container running. URL: http://localhost:8000/
docker run -d --name emission-frontend -p 3000:80 emission-frontend:latest
echo Frontend container running. URL: http://localhost:3000/