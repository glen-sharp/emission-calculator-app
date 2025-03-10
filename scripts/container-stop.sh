#!/usr/bin/env bash

docker stop emission-frontend && docker rm emission-frontend

docker stop emission-api && docker rm emission-api